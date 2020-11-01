CZ4045 Assignment 1
===================

In this github repository there are 3 different section.
1. Domain Specific Dataset Analysis
2. Development of a (Noun - Adjective) Pair Ranker
3. Application based on the reviews dataset collected in [2.]

Before starting for the each specific section, let's see how to install the required library used in this Project.

Installation
------------
Below are step by step guide to clone this repository and install the required library used.
1. Make sure you've installed git in your computer.
2. Clone this specific repository.
    1. If you have the Github Desktop, just find the "Clone Repository" in the File menu and enter this "https://github.com/dennisstevanus/cz4045.git".
    2. If you are using Github from terminal, you can just enter this code `git clone https://github.com/dennisstevanus/cz4045.git`.
3. If you like to you can setup an virtual environment
    1. Making the the virtual environment run this on terminal `python3 -m venv venv`
    2. Activate the Virtual environment `source venv/bin/activate`
4. Install the required library by running this in terminal `pip install -r requirements.txt`
5. Install the corpus needed for the Python NLTK
    1. Run the nltk_download python script `python3 nltk_download.py`
    2. Choose the **all** for the all packages under the **Collections** tab. Download All Packages

Content information
------------
*   `data`: Contains all the dataset used in this project
*   `data_analyisis`: Contains the code used to analyze the data in this project
*   `demo_server`: Contains the demo server for the Application [3.]
*   `model_training`: Contains the jupyter notebook code to train and fine-tune the model for [3.] 
*   `results`: Contains the `.json` file containing the result of the NLP tasks performed on each document 
*   `utils`: Contains several python scripts developed by our team to perform the required tasks. 
    Below are the description of each script and its usage guide: 
    *   `NLPToolkit`: A module developed by our team to perform NLP tasks 
    (Tokenization, Stemming, Sentence Segmentation, and POS Tagging) from a given string and save the result into a `json` format.
    To use the module, just call `NLPToolkit("insert your document as a single string here")`.  
    You can also run the `NLPToolkit.py` directly from the terminal(ex. cmd, bash) to try and test it: 
        ```bash
        python NLPToolkit.py
        ```
        The output will be in form of a json like below: 
        ```python
        {'pos_tagger': [[('The', 'DT'), ('tower', 'NN'), ('.', '.')],
                        [('Calamity', 'NN'), ('.', '.')]],
         'segmented_sentence': ['The tower.', 'Calamity.'],
         'stemmed_token': ['tower', '.', 'the', 'calam'],
         'token': ['tower', '.', 'The', 'Calamity'],
         'unique_identifier': ''}
        ```
        Following are the descriptions for the json result: 
        *   `pos_tagger`: Contains the result of the pos-tagger. 
        *   `segmented_sentence`: Contains the result of the segmented sentence as a list of string.
        *   `stemmed_token`: Contains the stemmed token in the form of a list of words. 
        *   `token` : Contains the tokens from the document in form of a list of words. 
        *   `unique_identifier`: Contains the title of the document if it is given to the toolkit. 
        
    *   `PairGetter`: A module developed by our team to read through the documents and calculate all possible pairs of <Noun- Adjective>, 
    as well as their respective number of occurrences.
    You can run the `PairGetter.py` directly from the terminal(ex. cmd, bash) to try and test it:
        ```bash
        python PairGetter.py
        ```  
        The output will be in form of list of items shown below: 
        ```python
        [('Netflix',
          {'adj_count': 64,
           'adj_list': {"'free": 1,
                        '3-4': 1},
           'counter': 41,
           'occurrences': [(1, 0), (2, 0)],
           'review_appearance': 20}
         ), ...]
        ```
        Each item in the list is a tuple of (Noun, `Dict`), \
        where `Dict` is a dictionary containing the following items: 
        *   `counter`: Showing the number of nouns occurring in the documents 
        *   `occurences`: Listing the location of each occurrence of a noun in the documents by (document no, sentence no), starting from index 0. 
        *   `adj_count`: Showing the number of adjectives accompanying the noun in the same sentence. 
        *   `adj_list`: Containing a dictionary that listed each adjective accompanying the noun in the same sentence as well as their respective number of occurences. 
        *   `review_appearance`: Number of distinct reviews the noun has appeared. 
    *   `PairRanker`: A module developed by our team to calculate scores and rank each <Noun- Adjective> pairs obtained from `PairGetter.py`.  
    You can run the `Pairranker.py` directly from the terminal(ex. cmd, bash) to try and test it:
        ```bash
        python PairRanker.py
        ```
        The output will be the ranking of the pairs obtained from `PairGetter.py` as well as the score of that pairs.
        Below is the example of the output: 
        ```
        Final results:
        1. < Netflix - new > with score of 792.0
        2. < movies - new > with score of 421.2
        3. < Netflix - bad > with score of 266.0
        4. < movies - bad > with score of 98.80000000000001
        5. < series - old > with score of 93.60000000000001
        ``` 
        Each pair in the ranking above is in the format of < Noun - Adjective > 
        
    Note: Make sure you have your terminal on the correct folder (`./utils/`) before running the command shown above. It can be done using `cd utils` if your terminal is currently pointing to the project directory. 
*   `web_scraper`: Contains the web scrapers used to automatically scrape the websites used in this project and convert it to a `document`(single long string) so that it can be automatically processed by `NLPToolkit`. 
    Just run the script in in order to automatically scrape and process the data from the websites.
     
    For example, to run the scraper for stackoverflow documents: 
    ```bash
    python stackoverflow_scraper.py
    ```
    Note: Make sure you have your terminal on the correct folder (`./web_scraper/`) before running the command shown above. It can be done using `cd web_scraper` if your terminal is currently pointing to the project directory. 
*   `nltk_download.py`: Contains the script to download the required contents for NLTK to run.

Note: If your default `python` is 2.7, you may need to run using command `python3` instead. 
Python version can be checked using `python --version`.  

Domain Specific Dataset Analysis
--------------------------------
Is it needed?

#### NLTK Toolkit ####
`Please input details here`

#### Jupyter Data analysis ####
Is it needed?

Application for the (Noun - Adjective) Pair Ranker
--------------------------------------------------
`Please input more details here`
