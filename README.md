# walmart-commodity-benchmark

How to use:
run Cereals_on_Walmart.py to update (if not existed in the current directory, create) Cereal_Data.csv, Ranking_and_Reviews.csv,  Ranking_and_Star.csv.

Cereal_Data gives real-time snapshots of numbers of all/top3 items for each brand in the list
[Cheerios Kashi Kellogg's Post Other]
given the search word "cold cereal" and "cereal".

Ranking_and_Reviews records ranking and number of reviews for each item when the program is run.
Ranking_and_Star records ranking and stars for each item (whose star information is not missing) when the program is run.

Run Cereal_Analytics to answer to following questions:

1) Given a set of competitor brands, for a given time range, for a given search term, what percentage of search results are owned by each brand?

2) Given a set of competitor brands, for a given time range, for a given search term, what percentage of the top 3 search results are owned by each brand?

3) Is there a correlation between the number of reviews and search ranking?

4) Is there a correlation between the rating and search ranking?
