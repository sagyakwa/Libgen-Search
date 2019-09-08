from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def textbook_request():
	return render_template('home_page.html')


@app.route('/faq', methods=['GET', 'POST'])
def faq():
	return render_template('faq.html')


if __name__ == '__main__':
	app.run()
