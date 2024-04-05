# Moody's Search App 🌐

Moodys-Search-App is a web application built on Streamlit, designed for easy document discovery and hosted on Google Cloud Run. It offers a user-friendly, efficient UI for document discovery.

## 🛠 Local Development and Testing

Gear up for development with these steps:

1. **Clone the Repository**

   Get the code on your machine:
   ```bash
   git clone https://github.com/arunpshankar/Moodys-Search-App.git
   cd Moodys-Search-App
   ```

2. **Create a Virtual Environment**

   Isolate your project by creating a virtual environment:
   ```bash
   python3 -m venv .moodys-search
   source .moodys-search/bin/activate
   ```

3. **Upgrade pip**

   Keep pip fresh:
   ```bash
   python3 -m pip install --upgrade pip
   ```

4. **Install Dependencies**

   Grab all the needed packages:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set the PYTHONPATH**

   Make your app known to Python:
   ```bash
   export PYTHONPATH=$PYTHONPATH:app/
   ```

6. **Fire Up the Application**

   Leap into action:
   ```bash
   cd app
   streamlit run src/app/app.py
   ```

Here's a rewritten version of your instructions in Markdown format for inclusion in a GitHub README file:

---

## Setting Up Company Name Embedding with FAISS

When updating your website's search feature to include new entities, follow these steps:

1. **Update the Entities Data**:
   - Add a new JSONLines file containing the new entities to `./data/entities.jsonl`.
   - Optionally, create a `test_entities.jsonl` in the same directory to include sample variants similar to what is shown in the existing `test_entities.jsonl` file.

2. **Generate the FAISS Index**:
   - Execute the following command:
     ```
     python src/embed/encode.py
     ```
   - This script processes the company names and updates the index files in `./data/faiss_index`:
     - `index.faiss`
     - `index.pkl`

3. **Testing Individual Cases**:
   - To test individual test cases, run:
     ```
     python src/embed/match.py
     ```

4. **Run Bulk Tests**:
   - To evaluate all entities alongside their variants, use:
     ```
     python src/embed/test.py
     ```
   - This module tests for 20 entities, each with 5 variants (representing potential user search terms). It assesses success based on the top match resolution via semantic search and computes coverage (accuracy).

By following these instructions, you can efficiently update and maintain the accuracy of your search functionalities using FAISS indexing.



## 🚀 Deployment to Google Cloud Run

Take your app to the clouds with these deployment steps:

1. **Launch Vertex AI Workbench**

   Start by launching a Vertex AI Workbench instance.

2. **Clone the Repository**

   Bring the project into your workspace:
   ```bash
   git clone https://github.com/arunpshankar/Moodys-Search-App.git
   cd Moodys-Search-App
   ```

3. **Deploy with Notebook**

   Navigate through `deploy.ipynb` to build, push, and deploy:
   - Build a Docker container with the provided `Dockerfile`.
   - Push the container to Google Container Registry (GCR).
   - Deploy your containerized app to Cloud Run.

