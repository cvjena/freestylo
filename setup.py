from setuptools import setup

if __name__ == "__main__":
    try:
        setup(use_scm_version={"version_scheme": "no-guess-dev"})
    except:
        print("Error: setup.py failed")
        raise
