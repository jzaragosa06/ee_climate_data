from dotenv import load_dotenv
import os

load_dotenv()
print(f"project: {os.getenv("PROJECT")}")