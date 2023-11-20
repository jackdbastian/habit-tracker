import xmltodict
import sqlite3

DB_PATH = '../pocketbase/pb_data/data.db'
XML_FILE_PATH = 'raw/all-releases.xml'
DELETE_QUERY = 'DELETE FROM releases; DELETE from artists; DELETE FROM companies; DELETE from artists_to_release; DELETE from companies_to_release'

# connect to pocketbase db
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# delete any existing data in the tables
cur.executescript(DELETE_QUERY)
con.commit()

# check if the record you are trying to insert already exists
def needs_insert(tbl_name, data):
    pk = list(data.keys())[0]
    query = f'SELECT {pk} FROM {tbl_name} WHERE {pk} = {data[pk]} LIMIT 1'
    cur.execute(query)
    if cur.fetchone():
        return False
    else:
        return True

# function for inserting data from the release into appropriate table
def insert_into_db(tbl_name, data):
    insert_statement = f"INSERT INTO {tbl_name} ({', '.join(data.keys())}) VALUES ({', '.join(['?' for _ in data.values()])})"
    cur.execute(insert_statement, tuple(data.values()))
 
# load raw xml
with open(XML_FILE_PATH, 'r') as xml_file:
    all_releases = xmltodict.parse(xml_file.read())['releases']['release']

# iterate through releases and pull out relevant data into appropriate lists
for release in all_releases:
    # only parse if it is the main release (to prevent duplication)
    if 'master_id' in release and release['master_id']['@is_main_release'] == 'true':
        # 'released' is the release year, only some releases have it
        if 'released' in release: 
            # TODO: properly format dates, switch '00' to '01' and add '01-01' to dates with just a year
            release_dict = {
                'release_id': release['@id'],
                'release_name': release['title'],
                'release_date': release['released']
            }
        else:
            release_dict = {
                'release_id': release['@id'],
                'release_name': release['title'],
                'release_date': None
            }
        
        insert_into_db('releases', release_dict)

        # are there artists?
        if release['artists'] != None:
            artists_data = release['artists']['artist']

            # check to see if there is a single artist (dict) or multiple (list)
            if type(artists_data) == dict: 
                artist_dict = {
                    'artist_id': artists_data['id'],
                    'artist_name': artists_data['name']
                }
                artist_to_release_dict = {
                    'artist_id': artists_data['id'],
                    'release_id': release['@id'],
                    # there is no 'role' key, unlike credits 
                    'role': 'Primary'
                }

                if needs_insert('artists', artist_dict):
                    insert_into_db('artists', artist_dict)

                insert_into_db('artists_to_release', artist_to_release_dict)
            else:
                # if it is not a single dictionary, loop through the list of dicts and do the same as above
                for artist in artists_data:
                    artist_dict = {
                        'artist_id': artist['id'],
                        'artist_name': artist['name']
                    }
                    artist_to_release_dict = {
                        'artist_id': artist['id'],
                        'release_id': release['@id'],
                        'role': 'Primary'
                    }
                    if needs_insert('artists', artist_dict):
                        insert_into_db('artists', artist_dict)

                    insert_into_db('artists_to_release', artist_to_release_dict)
            
        # are there credits? (e.g. 'Vocals' or 'Mixed By')
        if release['extraartists'] != None:
            credits_data = release['extraartists']['artist']

            # same structure as artists above
            if type(credits_data) == dict:
                credit_dict = {
                    'artist_id': credits_data['id'],
                    'artist_name': credits_data['name']
                }
                # TODO: break out multiple roles
                credit_to_release_dict = {
                    'artist_id': credits_data['id'],
                    'release_id': release['@id'],
                    'role': credits_data['role']
                }            
                if needs_insert('artists', credit_dict):
                    insert_into_db('artists', credit_dict)
                insert_into_db('artists_to_release', credit_to_release_dict)
            else:
                for credit in credits_data:
                    credit_dict = {
                        'artist_id': credit['id'],
                        'artist_name': credit['name']
                    }
                    credit_to_release_dict = {
                        'artist_id': credit['id'],
                        'release_id': release['@id'],
                        'role': credit['role']
                    }            
                    if needs_insert('artists', credit_dict):
                        insert_into_db('artists', credit_dict)
                    insert_into_db('artists_to_release', credit_to_release_dict)

        # are there labels?    
        if release['labels'] != None:
            label_data = release['labels']['label']

            # same structure as artists above
            if type(label_data) == dict:
                label_dict = {
                    'company_id': label_data['@id'],
                    'company_name': label_data['@name']
                }
                label_to_release_dict = {
                    'company_id': label_data['@id'],
                    'release_id': release['@id'],
                    'role': 'Label'
                }
                if needs_insert('companies', label_dict):
                    insert_into_db('companies', label_dict)
                insert_into_db('companies_to_release', label_to_release_dict)
            else:
                for label in label_data:
                    label_dict = {
                        'company_id': label['@id'],
                        'company_name': label['@name']
                    }
                    label_to_release_dict = {
                        'company_id': label['@id'],
                        'release_id': release['@id'],
                        'role': 'Label'
                    }
                    if needs_insert('companies', label_dict):
                        insert_into_db('companies', label_dict)
                    insert_into_db('companies_to_release', label_to_release_dict)

        # are there companies?
        if release['companies'] != None:
            company_data = release['companies']['company']

            # same structure as artists above
            if type(company_data) == dict:
                company_dict = {
                    'company_id': company_data['id'],
                    'company_name': company_data['name']
                }
                company_to_release_dict = {
                    'company_id': company_data['id'],
                    'release_id': release['@id'],
                    'role': company_data['entity_type_name']
                }
                if needs_insert('companies', company_dict):
                    insert_into_db('companies', company_dict)
                insert_into_db('companies_to_release', company_to_release_dict)
            else:
                for company in company_data:
                    company_dict = {
                    'company_id': company['id'],
                    'company_name': company['name']
                    }
                    company_to_release_dict = {
                        'company_id': company['id'],
                        'release_id': release['@id'],
                        'role': company['entity_type_name']
                    }
                    if needs_insert('companies', company_dict):
                        insert_into_db('companies', company_dict)
                    insert_into_db('companies_to_release', company_to_release_dict)

con.commit()
