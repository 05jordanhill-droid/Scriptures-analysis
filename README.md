# Overview

The data set I am analyzing is of the Old Testament, New Testament, Book of Mormon, Doctrine and Covenants, and Pearl of Great Price. They iterate verse by verse each holding the volume name, book name, chapter number, and verse number.

[Database Link](https://www.kaggle.com/datasets/molecman/scriptures)

My purpose for writing this software has been to learn and practice how to work with pandas in data analysis. It has also allowed me to utilize a personal passion, being the Scriptures, into a program where I can analyze the word usage in said Scriptures.

[Software Demo Video](https://youtu.be/NXKdg0fmVD8)

# Data Analysis Results

Question 1: How many occurences of a given word appears in a given selection of Scripture and how does that word count compare to other selections?

Answer 1: While the answer depends on the given word and given selections, for testing, I compared the Book of Mormon with the New Testament using the word repent. The given results are as follows:

    BoM has "repent" 205 times
    NT has "repent" 24 times
    "repent" appears in BoM 8.541666666666666 times more than NT
    "repent" appears in NT 0.11707317073170732 times less than BoM

Question 2: What is the density of a given word within a given selection of Scripture and how does that density compare to other selections?

Answer 2: While the answer depends on the given word and given selections, for testing, I compared the Book of Mormon with the New Testament using the word repent. The given results are as follows:

    BoM has "repent" at a density of %0.07663007113513433
    NT has "repent" at a density of %0.013284255389809868
    BoM "repent" density is 5.768488250678769 times more than NT "repent" density
    NT "repent" density is 0.17335564476227053 times less than BoM "repent" density

Question 3: What are the most used words within a given selection of Scripture?

Answer 3: While the answer depends on the given selection, for testing, I analyzed the Book of Mormon. The top 10 words used within in the Book of Mormon along with their data are as follows:

    Total Word Count: 267519
    Word            | Count    | Density
    -----------------------------------------------------------
    The             | 19079    | %7.131829888718184
    And             | 16295    | %6.091156142180555
    Of              | 11664    | %4.360064144976619
    That            | 6868     | %2.567294285639525
    To              | 6428     | %2.402819986617773
    They            | 4478     | %1.6738997977713732
    In              | 3688     | %1.378593669982319
    Unto            | 3624     | %1.3546701355791553
    I               | 3316     | %1.239538126263929
    He              | 3173     | %1.1860839790818596

# Development Environment

The primary tool that I used to help build this software was VSCode.
I used the assistance of ChatGPT to help understand unfamiliar syntaxing for Python.
I also used the assistance of ChatGPT to help troubleshoot roadblocks integrating and using Pandas.

I used Python for the language of this project. The library module, Pandas, was used for the primary method of iterating through and finding selections of Scripture within a given search specification to further analyze. Math was used 

# Useful Websites

* [Python Pandas Tutorial](https://www.youtube.com/watch?v=EXIgjIBu4EU)
* [ChatGPT - Python/Pandas Questions](https://chatgpt.com/share/6b0a244d-5d94-83e8-99f0-6a07a5069b71)

# Future Work

* Implement deeper analyses using percentages rather than exactness in word comparisons.
* Implement an 1830's (or other year if necessary) thesaurus API for deeper analyses.
* Improve overall runtime as it iterates through the large amounts of data.