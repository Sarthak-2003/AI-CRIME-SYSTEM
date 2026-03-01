import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

df = pd.read_csv("D:\\MAJOR-2\\Python Files\\crime_dataset_india.csv")
df = df.dropna(subset=["Crime Description", "Weapon Used"])

ipc_mapping = {
    "Murder": "IPC 302",
    "Rape": "IPC 376",
    "Theft": "IPC 378",
    "Kidnapping": "IPC 363",
    "Robbery": "IPC 392",
    "Assault": "IPC 351",
    "Dowry Death": "IPC 304B",
    "Cheating": "IPC 420",
    "Rioting": "IPC 147",
    "Cyber Crime": "IT Act 66"
}

model = make_pipeline(TfidfVectorizer(), MultinomialNB())

X = df["Crime Description"]
y = df["Weapon Used"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=20)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
report = classification_report(y_test, y_pred)

df["Predicted Crime"] = model.predict(df["Crime Description"])
df["IPC Section"] = df["Predicted Crime"].map(ipc_mapping)

crime_summary = df["Predicted Crime"].value_counts()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

crime_summary.plot.pie(ax=ax1, autopct='%1.1f%%', startangle=140, colors=plt.cm.tab20.colors)
ax1.set_title("Distribution of All Crime Types in India as discussed", fontsize=14)
ax1.set_ylabel("")

ax2.axis('off')
ax2.set_title("Report (Weapon Used Prediction)", fontsize=14, loc='left')
ax2.text(0, 1, report, fontsize=13, fontfamily='monospace', va='top')

plt.tight_layout()
plt.show()
