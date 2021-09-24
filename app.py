import os

from flask import (Flask, redirect, render_template, request, url_for)
import workos
from workos import client as workos_client
from workos import portal


# Flask Setup
DEBUG = False
app = Flask(__name__)

# WorkOS Setup
workos.api_key = os.getenv('WORKOS_API_KEY')
workos.project_id = os.getenv('WORKOS_CLIENT_ID')
workos.base_api_url = 'http://localhost:7000/' if DEBUG else workos.base_api_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/provision_enterprise', methods=['POST'])
def provision_enterprise():

    organization_name = request.form['org']
    print(organization_name)
    organization = request.form['domain']
    print(organization)
    organization_domains = organization.split()
    print(organization_domains)

    organization = workos_client.organizations.create_organization({
        'name': organization_name,
        'domains': organization_domains
    })

    # You should persist `organization['id']` since it will be needed
    # to generate a Portal Link.
    global org_id
    org_id = organization['id']
    print(org_id)

    return render_template('org_logged_in.html')

@app.route('/sso_admin_portal', methods=['GET', 'POST'])
def sso_admin_portal():
    portal_link = workos_client.portal.generate_link(
      organization=org_id, intent='sso'
    )
    return redirect(portal_link['link'])

@app.route('/dsync_admin_portal', methods=['GET', 'POST'])
def dsync_admin_portal():
    portal_link = workos_client.portal.generate_link(
      organization=org_id, intent='dsync'
    )
    return redirect(portal_link['link'])
