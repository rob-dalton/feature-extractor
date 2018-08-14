TESTS=$(wildcard tests/*.py)

.PHONY: test
test:	
	@- $(foreach TEST,$(TESTS), \
			echo === Running test: $(TEST); \
			python -m unittest $(TEST); \
		)

data:
	# TODO: Test opinion-lexicon-English downloads, decompresses
	mkdir ./data
	wget -O ./data/meta_Patio_Lawn_and_Garden.json.gz http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/meta_Patio_Lawn_and_Garden.json.gz
	wget -O ./data/reviews_Patio_Lawn_and_Garden_5.json.gz http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Patio_Lawn_and_Garden_5.json.gz 
	wget -O ./data/ http://www.cs.uic.edu/~liub/FBS/opinion-lexicon-English.rar
	gunzip ./data/meta_Patio_Lawn_and_Garden.json.gz
	gunzip ./data/reviews_Patio_Lawn_and_Garden_5.json.gz
	unrar e ./data/opinion-lexicon-English.rar ./data/

database:
	mongoimport --db amazon_reviews --collection reviews ./data/reviews_Patio_Lawn_and_Garden_5.json
	mongoimport --db amazon_reviews --collection metadata ./data/meta_Patio_Lawn_and_Garden.json
