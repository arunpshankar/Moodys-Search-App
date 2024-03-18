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

