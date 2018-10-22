from flask import Flask, redirect
from flask_graphql import GraphQLView
from schema.schema import make_schema
import argparse

app = Flask(__name__)
parser = argparse.ArgumentParser()
parser.add_argument("db", help="Database connection string")
parser.add_argument("top_level", help="Top level field names", nargs="+")

args = parser.parse_args()

@app.route("/")
def home():
    return redirect("/graphql")

schema = make_schema(args.db, args.top_level)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)


if __name__ == "__main__":
    app.run()
