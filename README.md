# NIPS2017

NIPS2017 is a Python 3 package used for collecting and preprocessing publications from [NIPS2017](https://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017) conference.
It also can be used as a basis for preprocessing publications from the [previous NIPS](https://papers.nips.cc/) conferences.

All ready files can be found [`here`](https://drive.google.com/open?id=1LCdSrh--qPX5myem1fh6lWfH3Qv5hmgq)

## Requirements
- Python 3
- Python 3 packages (all can be install using `pip install [package_name]`):
  - [requests](http://docs.python-requests.org/en/master/)
  - [bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
  - [json](https://docs.python.org/3/library/json.html)
  - [re](https://docs.python.org/3/library/re.html)
  - [subprocess](https://docs.python.org/3/library/subprocess.html)
  - [enchant](https://pypi.org/project/pyenchant/)
  - [spacy](https://spacy.io/)
  - [collections](https://docs.python.org/3.3/library/collections.html)
  - [nltk](https://www.nltk.org/)
  - [urllib](https://docs.python.org/3/library/urllib.html)
  
## More about NIPS2017
  
### Collecting Data

Scripts related to collecting data are located in [GetData](https://github.com/nuwanda57/NIPS2017/tree/master/GetData) folder.

1) [`dovnload.py`](https://github.com/nuwanda57/NIPS2017/blob/master/GetData/download.py) provides functionality to:
  - collect all references to the publications into **articles_refs.json** file (*appears in the working directory*)
  - collect all the articles names into **articles_pages.json** file (*appears in the working directory*)
  - download the publications texts into **Articles** directory (*the folder must be created before script execution*)
  - download the abstracts into **Abstracts** directory (*the folder must be created before script execution*)
  - download the reviews into **Reviews** directory (*the folder must be created before script execution*)
  
2) [`authors.py`](https://github.com/nuwanda57/NIPS2017/blob/master/GetData/authors.py) provides functionality to:
  - save all the authors names into json files in **Authors1** directory (*the folder must be created before script execution*)

### Processing Data

Scripts related to collecting data are located in [ProcessData](https://github.com/nuwanda57/NIPS2017/tree/master/ProcessData) folder.

1) [`divide_articles.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/divide_articles.py) (The script must be executed in the directory where **articles_refs.json**, **Articles**, **Reviews** are located.) provides functionality to:
  - convert pdf files into txt files and save them into **ArticleText** directory (*the folder must be created before script execution*)
  - convert reviews from html format into txt files and save them into **ReviewText** directory (*the folder must be created before script execution*)

#### Text Processing
2) [`TextProcessing/add_empty_line_before_number.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/TextProcessing/add_empty_line_before_number.py) makes text files more readable and easy-to-process. The path to **articles_refs.json** and **ArticleText** mist be `./..`. In the working directory a folter **OnlyText1** must be created.

3) [`TextProcessing/section_processing.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/TextProcessing/sections_processing.py) makes text files more readable and easy-to-process. Must be executed in the same directory as the previous script. Directories **OnlyText1**, **2**, **3**, **4**, **5**, **6**, **7** and **OnlyText** must be created before the execution. Divides text into sections (3 line breaks) and subsections (2 line breaks). Not 100% accurate division. Actions from user are required: look for questions on a command line and answer 0 - *No*, 1 - *Yes* from a keyboard. After the execution copy all files from the **OnlyText7** directory into **OnlyText** directory.

4) [`TextProcessing/intro_related_conclusion_ackno.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/TextProcessing/intro_related_conclusion_ackno.py) find introduction, related works, conclusion, acknowledgements in each text file and save them into **Sections/IntroText**, **Sections/RelatedText**, **Sections/ConclusionText**, **Sections/AcknowledgementsText**. As always, these deirectories must be created before the execution.

5) [`TextProcessing/clean.py`](https://github.com/nuwanda57/NIPS2017/edit/master/ProcessData/TextProcessing/clean.py) delete all non English words from the text and save the results into **CleanText1** directory. `./../TextProcessing/OnlyText/` and `./../articles_refs.json` are required.

### Statistics

1) [`statistics.py`](https://github.com/nuwanda57/NIPS2017/blob/master/Statistics/statistics.py) lists most common n-grams of 2, 3, 4, 5 words. And saves the results into **Statistics1** directory. Directory **CleanText1** is required.

### CSV Format

4) [`folder_main_table.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/folder_main_table.py), [`location_main_table.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/location_main_table.py), [`visual_main_table.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/visual_main_table.py) create different versions of representation of resultive data.

### Additional Scripts/Files

1) [`bibliography_find.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/bibliography_find.py) searchs for a bibliography item in Google Scholar.

2) [`google_bibliography.py`](https://github.com/nuwanda57/NIPS2017/blob/master/ProcessData/google_bibliography.py) searchs for a bibliography item in Google (Google Developer key is required).

3) [`Data`](https://github.com/nuwanda57/NIPS2017/tree/master/Data) contains jsons of bibliography from those articles that cannot be processed automatically.
