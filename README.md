CZ4045 Assignment 1
===================

In this github repository there are 3 different subtasks: 
1. Domain Specific set Analysis
2. Development of a (Noun - Adjective) Pair Ranker
3. Application based on the reviews dataset collected in [2.]

Before starting for the each specific section, let's see how to install the required library used in this Project.

Installation
------------
Below are step by step guide to clone this repository and install the required library used.
1.  Make sure you've installed git in your computer. (Note: Skip to step 4 if you already have the code from the submission zip and just open a terminal in the source code directory instead.)
2.  Clone this specific repository. 
    1. If you have the Github Desktop, just find the "Clone Repository" in the File menu and enter this "https://github.com/dennisstevanus/cz4045.git".
    2. If you are using Github from terminal, you can just enter this code `git clone https://github.com/dennisstevanus/cz4045.git`.
3.  Go to the the repository directory. For example, after running the step 2.2 above, you can use `cd cz4045`. This will be referred as `project root directory`. 
4.  Setup an virtual environment (optional). 
    The following are the tutorial on how to setup venv on Unix machine. For windows or more information, see this [link](https://docs.python.org/3/tutorial/venv.html)
    1. Making the the virtual environment:
        run this on terminal `python3 -m venv venv`
    2. Activate the Virtual environment `source venv/bin/activate`
5.  Install the required library by running this in terminal `pip install -r requirements.txt`
6.  Install the corpus needed for the Python NLTK
    1. Run the nltk_download python script `python3 nltk_download.py`
    2. Choose the **all** for the all packages under the **Collections** tab. Download All Packages
7.  **Important!** Setup the `PYTHONPATH` to include `project root directory` in the the `PYTHONPATH`. Tutorial on how to set this up is on this [link](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html). 
    Otherwise, it can also be done by using `PyCharm IDE` and then using the IDE's [code run assistance](https://www.jetbrains.com/help/pycharm/code-running-assistance-tutorial.html) which by default add `project root directory` to the `PYTHONPATH`. 

Content information
------------
*   `data`: Contains all the dataset used in this project
*   `data_analyisis`: Contains the code used to analyze the data in this project
    *   `data_analysis.ipynb`: It's a Jupyter notebook that containing the code used to analyze the data for the [3.1]. You can run the file in jupyter notebook by     opening the jupyter notebook on terminal and try to see the analysis there.
        ```bash
        jupyter notebook
        ```
*   `demo_server`: Contains the demo server for the Application [3.]
*   `model_training`: Contains the jupyter notebook code to train and fine-tune the model for [3.3] 
    * `FineTuning_of_GPT_2.ipynb`: It's a Jupyter notebook used to fine-tune the model of GPT-2. As it requires GPU, it is advised to upload this to Google Drive and use Google Colab to open (and fine-tune the model) instead.
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
    This is the script that is executed to get the values shown in the report for task [2.]
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

Application for the (Noun - Adjective) Pair Ranker
--------------------------------------------------
For the application, some extra steps are needed to run the program.
1.   Download the model from [here](https://entuedu-my.sharepoint.com/:u:/g/personal/skurnia001_e_ntu_edu_sg/EfgaJvvxNA5Br-BteyjWTA8BIZ0SkbPsmShY7DcEt5xHrQ?e=x92uTh)
2.   Extract the packaged model
3.   Put the extracted model in \demo_server\

In the end, the structure of the static folder of the demo server should look like this:
```
demo_server
|
- static
    |
    - checkpoint
        |
        - run2
            |
            - (many files)
```

After placing the model in the right place, just run the server by this command `python manage.py runserver`.

A webserver will be opened, and can be accessed (usually) at http://127.0.0.1:8000 .
From that link, there will be a text box, which is the user input for the prefix of the review. After generating the 
review, the end result will contain those input as the prefix.


Error troubleshooting
------------

*   If you encountered `ImportError` messages, most likely you have missed Installation step 5. Please do the instructions described in step 5.
*   If you encountered `ModuleNotFoundError` messages like this: 
    ```
    ModuleNotFoundError: No module named 'web_scraper'
    ```
    most likely you have not done the Installation step 7. Please do the instructions described in step 7.
*   If you encountered `FileNotFoundError` or any other errors when running the demo server, most likely you missed the installation step for the Pair Ranker application or there are missing files in your project directory. Please try to follow the steps described in the instructions above. 
