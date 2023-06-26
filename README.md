# Genius Music Search

Project for CPEG457: Search and Data Mining
A music search engine that searches through top artists from Genius.com's artists page with the intent of searching songs on lyrics &amp; 'vibe'. The program iterates through each artist, their top albums, and each song from the album &amp; scrapes the lyrics &amp; description using Beautiful Soup...  

<ins> Motivation </ins>

Some people try to find new music, but there are only limited strategies, which include:  
*Hearing somewhere  
*Curated playlists  
*Radio  
*Recommendations  

While these are great, sometimes users want to find extremely specific songs. Maybe they are thinking of a certain word, or a vibe, or an instrument used in a song. The idea behind my project would be to capitalize on this.  

<ins>Goal</ins>  

The goal of this project is to:  
*Curate current top albums (according to genius.com)  
*Allow users to search based on lyrics & song descriptions  
*Output the link & name of the song  

While it would technically be possible, and not difficult, to gather every listed artist & all of their albums, it would take a long time for the code to retrieve all of this data. Because of this, I wanted to use the top 2 albums from the top 20 artists from a-z. In the end, I only gathered around 100 artists worth of data, which is still enough data to search through for the purpose of this project.  

<ins>Implementation</ins>  

I started by creating the retrieval for the artists. I began by attempting to retrieve the data from wikipedia, but this was difficult for 3 reasons:  

They were categorized by genre rather than by letter, which made it difficult to sift through which artists I would want to include:  

Due to the nature of Wikipedia, each page could (and often do) have entirely different page structures, so it is difficult to create a scheme that would work unanimously.  
There is no listing based on popularity, so I would have to sift through many unknown artists, many of which have very limited listed on their individual pages, in order to get the popular artists.  

Because of this, I used genius.com’s popular artist pages. I would then sift through the top 20 artists listed on the page, which are categorized as “most popular”. I then could sift through each artist page to get individual albums, and could retrieve the songs from each album, and finally could get the lyrics & description of each song.   

I decided to use beautiful soup to retrieve the data from each page, as it is well documented online. The main difficulty in retrieving all of this data was finding where the information was held. Genius.com is obviously not a basic html page, so I had to differentiate between multiple listings of the same referenced link to find which one was relevant. Another issue I had with this was that, for some reason, the occasional song was either not structured the same way or had no lyrics/description, so I had to add a check for this.  

After creating these functions, I could then call them for each artist. I stored the lyrics, links, and song names in 3 arrays. The index of each would be matched, i.e index 0 would be the first song, etc.   

Due to the run-time of the algorithm, I decided to use the pickle library, which allows me to store the lists into files. This is nice as, if the program were to crash, I can have the current lists saved. This also means that the retrieval code does not need to be ran every time a user wants to search.  

Next is the search code. I wanted to allow the user to search simply using their terminal & python (along with whatever libraries are needed). There are 2 parts: calculating the score for each word and searching through this score. To get the score, I used a TF-IDF pivoted normalization formula:  

(( 1 + ln(1+ln(tf)))/((1-s)+s*(dl/avdl))) * qtf * ln((N+1)/df)  

To implement this, I first attempted to use pandas to create a data frame. While this worked, it was extremely slow. I researched online and realized that numpy could be faster, so I switched to using a numpy 2d array.   

I also used a dictionary to store the words and the tf_idf, as it increased efficiency. I first stored each word in a dictionary, storing the number of unique words. I then calculated TF, which used the document length, average document length, as well as the term frequency, as well as a constant 0.2 I then calculated IDF, which simply used log(ndocs + 1 / df) Finally, I multiply the two values together for each word. I decided not to use query term frequency, as it would be more difficult to implement and not provide much for this use case.  

Finally, all I had left was to allow the user to create a query.  

I first lowercase all queries, as I wanted the searches to be case insensitive. I then create a score for each word that is searched compared to the tf_idf, and simply retrieve the index for the top 5, and finally return the top 5 name and links in order from most relevant to least.  

<ins>Evaluation</ins>  

Overall, the project works quite well. There are 2 primary issues in its current implementation:
1. The retrieval for lyrics takes quite a long time, at around 40 seconds per artists, which means, in an ideal situation, 40s * 20 albums per letter * 26 letters = 20800s / 60 ≈ 347 mins or over 4 hours. And, because of this,  
  
2. Limited amount of songs. Ideally, I would want every song available, but obviously I do not have the same storage that genius.com has. Even despite this, there are many popular artists that aren’t listed. (in letters more contentious such as k, compared to unpopular letters like q).  

After the lists of lyrics are saved, the search is quite fast. I am happy about this as when I was using pandas it would take quite a long time, up to an hour.  

<ins>Conclusion</ins>  
Overall, the music search program I have created is, while very simply, definitely useful. If users want to easily search through Genius’s list of music, without considering song names, this program could be more useful than their built-in search.   

I am satisfied with my ranking, as it considers both the lyrics and descriptions. This means sometimes songs I wouldn’t expect to be retrieved top their searches. I have found new songs I’ve never heard of by testing my program.  

I am also satisfied with my retrieval, as, despite its lengthy retrieval time, it is able to effectively gather all of the relevant information.  
