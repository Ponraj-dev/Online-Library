
from website import create_app
import flask_excel  as excel


if __name__=="__main__":
    app = create_app()

    app.app_context().push()
    app.run(debug=True)
