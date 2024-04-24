**AskScrappy: A Mental Health-Focused Chatbot for KSU Students**
===========================================================

**Overview**
-----------

AskScrappy is a specialized chatbot designed to improve the mental health of Kennesaw State University (KSU) students by providing accurate, relevant, and personalized advising throughout their college journeys.

**Checklist of Steps**
--------------------
### Step 0: Research and Planning
* [ ] Conduct research on mental health in college students and the role of chatbots in mental health support
* [ ] Identify the specific needs and concerns of KSU students
* [ ] Define the scope and objectives of AskScrappy

### Step 1: Data Collection

* [ ] Scrape data from:
	- [ ] RateMyProfessors.com: Collect data on KSU professors, including ratings and reviews.
	- [ ] KSU's subreddit: Collect data on student experiences, concerns, and advice.
	- [ ] KSU's website: Collect data on course offerings, curricula, and academic policies.
* [ ] Store scraped data in a database or data warehouse for later use.

### Step 2: Data Preprocessing

* [ ] Clean and preprocess scraped data to remove errors, inconsistencies, and irrelevant information.
* [ ] Transform data into a format suitable for training a language model.

### Step 3: Language Model Training

* [ ] Choose a Large Language Model (LLM) architecture, such as Llama 3, Phi3, Claude, GPT, Snowflake Arctic, etc.  
* [ ] Fine-tune the LLM on the preprocessed data to make it particularly good at answering questions undergraduate students at KSU may have.

### Step 4: Chatbot Development

* [ ] Design a conversational interface for AskScrappy, including a user-friendly input and output system.
  - Potential Platforms:
    + [Ollama](https://ollama.com/)
    + [Dialogflow](https://cloud.google.com/dialogflow?hl=en)
    + [Microsoft Bot Framework](https://botframework.com/)
    + [Rasa](https://rasa.com/docs/rasa/)
* [ ] Integrate the trained language model into the chatbot, allowing it to generate responses to user queries.
* [ ] Implement natural language processing (NLP) techniques to handle user input and intent detection
  - Potential Frameworks:
    + [NLTK](https://www.nltk.org/)
    + [spaCy](https://spacy.io/)
    + [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)

### Step 5: Course Planning and Recommendation

* [ ] Engineer prompting techniques to plan out courses most efficiently, taking into account:
	- Up-to-date curricula
	- RateMyProfessor reviews
	- Student's previously taken courses
	- Urgency to graduate/pain tolerance tradeoff

### Step 6: Testing and Evaluation

* [ ] Test AskScrappy with a diverse set of user queries and scenarios to ensure its accuracy and relevance.
* [ ] Evaluate the chatbot's performance using metrics such as response quality, response time, and user satisfaction.

### Step 7: Deployment and Maintenance

* [ ] Deploy AskScrappy on a suitable platform, such as a web application or mobile app.
* [ ] Try to host inference on [KSU's High Performance Compute Cluster](https://hpcdocs.kennesaw.edu/)
* [ ] Develop a plan for ongoing maintenance, including data updates, model fine-tuning, continuous improvement and bug fixes.


**Contributing:**
If you're interested in contributing to AskScrappy, please fork this repository and submit a pull request with your changes. We welcome contributions from developers, designers, and mental health professionals.
