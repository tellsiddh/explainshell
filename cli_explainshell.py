import argparse
import re
from explainshell import store
from explainshell.matcher import matcher

class FakeConfig:
    MONGO_URI = 'mongodb://localhost:27017'
    DBNAME = 'explainshell'
    DEBUG = True

def strip_html(html):
    return re.sub('<[^<]+?>', '', html).strip()

def main():
    parser = argparse.ArgumentParser(description="Explain a shell command like explainshell")
    parser.add_argument("command", nargs="+", help="Shell command to explain")
    args = parser.parse_args()

    cmdline = " ".join(args.command)
    if isinstance(cmdline, bytes):
        cmdline = cmdline.decode("utf-8")

    s = store.store(FakeConfig)
    m = matcher(cmdline, s)
    m.match()
    matches = m.allmatches

    if not matches:
        print("No explanation found.")
        return

    print(f"\n🔍 Explaining: {cmdline}\n")
    for match in matches:
        token = str(match.match or '').strip()
        explanation = match.text
        if isinstance(explanation, bytes):
            explanation = explanation.decode('latin1')

        explanation = strip_html(str(explanation).strip())



        if not token or not explanation:
            continue

        print(f"🔹 {token}\n    {explanation}")

if __name__ == "__main__":
    main()
