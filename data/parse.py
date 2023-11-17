import xmltodict
import pandas as pd

# load raw xml
with open('raw/all-releases.xml', 'r') as xml_file:
    all_releases = xmltodict.parse(xml_file.read())['releases']['release']

# initialize new lists of dicts
releases = []
artists = []
companies = []
artists_to_release = []
companies_to_release = []

# iterate through releases and pull out relevant data into appropriate lists
for release in all_releases:
    # only parse if it is the main release (to prevent duplication)
    if 'master_id' in release:
        if release['master_id']['@is_main_release'] == 'true':

            # create releases list
            # 'released' is the release year, only some releases have it
            if 'released' in release: 
                releases.append({
                    'release_id': release['@id'],
                    'release_name': release['title'],
                    'release_date': release['released']
                })
            else:
                releases.append({
                    'release_id': release['@id'],
                    'release_name': release['title'],
                    'release_date': None
                })

            # are there artists?
            if release['artists'] != None:
                artists_data = release['artists']['artist']

                # check to see if there is a single artist (dict) or multiple (list)
                if type(artists_data) == dict: 
                    # add to master artist list
                    artists.append({
                        'artist_id': artists_data['id'],
                        'artist_name': artists_data['name']
                    })
                    # add to artist to release mapping list
                    artists_to_release.append({
                        'artist_id': artists_data['id'],
                        'release_id': release['@id'],
                        # there is no 'role' key, unlike credits 
                        'role': 'Primary'
                    })
                else:
                    # if it is not a single dictionary, loop through the list of dicts and do the same as above
                    for artist in artists_data:
                        artists.append({
                            'artist_id': artist['id'],
                            'artist_name': artist['name']
                        })
                        artists_to_release.append({
                            'artist_id': artist['id'],
                            'release_id': release['@id'],
                            'role': 'Primary'
                        })
            
            # are there credits? (e.g. 'Vocals' or 'Mixed By')
            if release['extraartists'] != None:
                credits_data = release['extraartists']['artist']

                # same structure as artists above
                if type(credits_data) == dict:
                    artists.append({
                        'artist_id': credits_data['id'],
                        'artist_name': credits_data['name']
                    })
                    artists_to_release.append({
                        'artist_id': credits_data['id'],
                        'release_id': release['@id'],
                        'role': credits_data['role']
                    })            
                else:
                    for credit in credits_data:
                        artists.append({
                            'artist_id': credit['id'],
                            'artist_name': credit['name']
                        })
                        artists_to_release.append({
                            'artist_id': credit['id'],
                            'release_id': release['@id'],
                            'role': credit['role']
                        })            

            # are there labels?    
            if release['labels'] != None:
                label_data = release['labels']['label']

                # same structure as artists above
                if type(label_data) == dict:
                    companies.append({
                        'company_id': label_data['@id'],
                        'company_name': label_data['@name']
                    })
                    companies_to_release.append({
                        'company_id': label_data['@id'],
                        'release_id': release['@id'],
                        'role': 'Label'
                        })
                else:
                    for label in label_data:
                        companies.append({
                            'company_id': label['@id'],
                            'company_name': label['@name']
                        })           
                        companies_to_release.append({
                            'company_id': label['@id'],
                            'release_id': release['@id'],
                            'role': 'Label'
                        }) 

            # are there companies?
            if release['companies'] != None:
                company_data = release['companies']['company']

                # same structure as artists above
                if type(company_data) == dict:
                    companies.append({
                        'company_id': company_data['id'],
                        'company_name': company_data['name']
                    })
                    companies_to_release.append({
                        'company_id': company_data['id'],
                        'release_id': release['@id'],
                        'role': company_data['entity_type_name']
                    })
                else:
                    for company in company_data:
                        companies.append({
                            'company_id': company['id'],
                            'company_name': company['name']
                        })           
                        companies_to_release.append({
                            'company_id': company['id'],
                            'release_id': release['@id'],
                            'role': company['entity_type_name']
                        }) 

# put the list of dicts into dataframes and drop duplicates
releases = pd.DataFrame(releases).drop_duplicates()
artists = pd.DataFrame(artists).drop_duplicates()
companies = pd.DataFrame(companies).drop_duplicates()
artists_to_release = pd.DataFrame(artists_to_release).drop_duplicates()
companies_to_release = pd.DataFrame(companies_to_release).drop_duplicates()

# write dfs to csv
releases.to_csv('parsed/releases.csv', index=False)
artists.to_csv('parsed/artists.csv', index=False)
companies.to_csv('parsed/companies.csv', index=False)
artists_to_release.to_csv('parsed/artists_to_release.csv', index=False)
companies_to_release.to_csv('parsed/companies_to_release.csv', index=False)
