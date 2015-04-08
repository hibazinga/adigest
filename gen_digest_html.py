from jinja2 import Environment, FileSystemLoader
import db

def gen_html(data, first_name):
    env = Environment(loader=FileSystemLoader('/var/www/FlaskApp/FlaskApp/newsletter-email-template/templates'))
    #template = env.get_template('newsletter.html')
    template = env.get_template('1.html')
    output_from_parsed_template = template.render(digests = data, first_name = first_name)
    #print output_from_parsed_template
	
    return output_from_parsed_template

if __name__ == "__main__":
    gen_html()
