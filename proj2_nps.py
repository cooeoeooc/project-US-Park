#################################
##### Name: Zekun Zhao
##### Uniqname: zzekun
#################################

from logging import info
from bs4 import BeautifulSoup
import requests
import json
import time
import secrets
from requests_oauthlib import OAuth1


#from requests.models import Response, json_dumps # file that contains your API key



states={'alaska': 'ak', 'alabama': 'al', 'arkansas': 'ar', 'american samoa': 'as',
        'arizona': 'az', 'california': 'ca', 'colorado': 'co', 'connecticut': 'ct',
        'district of columbia': 'dc', 'delaware': 'de', 'florida': 'fl', 'georgia': 'ga',
        'guam': 'gu', 'hawaii': 'hi', 'iowa': 'ia', 'idaho': 'id', 'illinois': 'il',
        'indiana': 'in', 'kansas': 'ks', 'kentucky': 'ky', 'louisiana': 'la',
        'massachusetts': 'ma', 'maryland': 'md', 'maine': 'me', 'michigan': 'mi',
        'minnesota': 'mn', 'missouri': 'mo', 'northern mariana islands': 'mp',
        'mississippi': 'ms', 'montana': 'mt', 'national': 'na', 'north carolina': 'nc',
        'north dakota': 'nd', 'nebraska': 'ne', 'new hampshire': 'nh', 'new jersey': 'nj',
        'new mexico': 'nm', 'nevada': 'nv', 'new york': 'ny', 'ohio': 'oh', 'oklahoma': 'ok',
        'oregon': 'or', 'pennsylvania': 'pa', 'puerto rico': 'pr', 'rhode island': 'ri',
        'south carolina': 'sc', 'south dakota': 'sd', 'tennessee': 'tn', 'texas': 'tx',
        'utah': 'ut', 'virginia': 'va', 'virgin islands': 'vi', 'vermont': 'vt',
        'washington': 'wa', 'wisconsin': 'wi', 'west virginia': 'wv', 'wyoming': 'wy'}

def get_key(dict,value):
    return [k for k,v in dict.items() if v==value][0]
'''
Input a dictionary and a value, and get the key of the value.
----------
parameter: 
dict: dictionary
value: a value of the dictionary, in this case it's a string
----------
return

k: string, the corresponding key for the input value.

'''
MAP_KEY=secrets.API_KEY
MAP_SECRET=secrets.API_SECRET

oauth = OAuth1(MAP_KEY,
            client_secret=MAP_SECRET)


def load_cache(CACHE_FILENAME):
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict,CACHE_FILENAME):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()
    
    
def make_url_request_using_cache(url, cache):
    if url in cache: # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url)
        cache[url] = response.text # notice that we save response.text to our cache dictionary. We turn it into a BeautifulSoup object later, since BeautifulSoup objects are nor json parsable. 
        save_cache(cache,CACHE_FILENAME)
        return cache[url] # in both cases, we return cache[url]
'''
   Check the cache for a saved result for this url. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    
    Parameters
    ----------
    url: string
        The URL for the website
        
    cache: a cache file
    
    
    Returns
    -------
    cache[url]
        the results of the query as a dictionary loaded from cache
        JSON
'''
CACHE_FILENAME = "park_cache.json"


cache_file=load_cache(CACHE_FILENAME)

class NationalSite:
    def __init__(self,category,name,address,zipcode,phone,url=None):

        #if url is None:
        self.category=category
        self.name=name
        self.address=address
        self.zipcode=zipcode
        self.phone=phone.strip('\n')
        self.url=url
                        
            
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.

    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
        
    url:None
    '''


    def info(self):
        return self.name+' ('+self.category+'): '+self.address+ ' ' +self.zipcode
    
    '''
    function for print format
    --------------
    parameter:self
    
    return: a print format

    '''
class Nearbyplace():
    def __init__(self,name,category,street_address,city_name):
        self.name=name
        self.category=category
        self.street_address=street_address
        self.city_name=city_name
        '''a nearby place

    Instance Attributes
    -------------------
    category: string
        the category of a nearby place. 
        some sites have blank category.

    name: string
        the name of a nearby place .

    street_address: string
        the street_address of a nearby place 

    city_name: string
        the name of the city of a nearby place. 

    
    '''
        
        
    def info(self):
        return self.name+' ('+self.category+'): '+self.street_address+', '+self.city_name
    
    '''
    function for print format
    --------------
    parameter:self
    
    return: a print format

    '''
    
    



def build_state_url_dict():
    #CACHE_Dict=open_cache()
    dict_states={}
    base_url='https://www.nps.gov'
    state_url=base_url+'/index.htm'
    url_text=make_url_request_using_cache(state_url,cache_file)
    soup = BeautifulSoup(url_text,'html.parser')#this part I edit in 10/8th morning
    state_parent=soup.find('ul',class_="dropdown-menu SearchBar-keywordSearch")
    state_ls=state_parent.find_all('li',recursive=False)
    for state in state_ls:
        state_link_tag=state.find('a')
        state_path=state_link_tag['href']
        state_url=base_url+state_path
        state_name=state.get_text().lower()
        dict_states[state_name]=state_url
        



    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''

    return dict_states


def get_site_instance(site_url):  



    url_text=make_url_request_using_cache(site_url,cache_file)
    park_soup= BeautifulSoup(url_text,'html.parser')
    park_parent=park_soup.find('div',class_='Hero-titleContainer clearfix')
    park_name=park_parent.find('a',class_='Hero-title').get_text()
    try:
        park_category= park_parent.find('div',class_='Hero-designationContainer').find('span',class_='Hero-designation').get_text().strip()
    except:
        park_category='Not found category'
    if park_category=='':
        park_category='Not found category'

    park_footer_parent=park_soup.find('div',class_='ParkFooter')
    try:
        park_zip_code=park_footer_parent.find('p',class_='adr').find('span',class_='postal-code').get_text().strip()
    except:
        park_zip_code='Not found zipcode'
    try:
        park_address=park_footer_parent.find('p',class_='adr').find('span',itemprop='addressLocality').get_text() +', ' +park_footer_parent.find('p',class_='adr').find('span',itemprop='addressRegion').get_text()
    except:
        park_address='Not found address'
    try:
        park_phone=park_footer_parent.find('span',class_='tel').get_text()#sometimes exsit "xxxxx or xxxxx", need to consider it latter.
    except:
        park_phone='Not found phone number'
        

    park_instance=NationalSite(park_category,park_name,park_address,park_zip_code,park_phone)

  

    '''Make an instances from a national site URL.

    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov

    Returns
    -------
    instance
        a national site instance
    '''

    #print(park_instance.category,'this is instance cate!!!!')
    return park_instance

def get_sites_for_state(state_url):
    base_url='https://www.nps.gov'

    sites_instance_list=[]


    url_text=make_url_request_using_cache(state_url,cache_file)
    site_soup=BeautifulSoup(url_text,'html.parser') 
    park_parent=site_soup.find('div',id="parkListResults")
    park_name_ls=park_parent.find_all('h3')
    for park_name in park_name_ls:
        park_tag=park_name.find('a')
        park_name=park_tag.get_text()
        #park_name_list.append(park_name)
        park_path=park_tag['href']
        park_url=base_url+park_path+'index.htm'
        
        park_address=get_site_instance(park_url).address
     
      
        park_category=get_site_instance(park_url).category
        
        
        park_zip_code=get_site_instance(park_url).zipcode
        
        
        park_phone=get_site_instance(park_url).phone
            
        site_instance=NationalSite(park_category,park_name,park_address,park_zip_code,park_phone,park_url)# might be a problem right here
        sites_instance_list.append(site_instance)
    '''Make a list of national site instances from a state URL.

    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov

    Returns
    -------
    sites_instance_list:
        a list of national site instances
    '''

    return sites_instance_list


def make_request_api(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    response=requests.get(baseurl,params,auth=oauth)
    #print(response)# good response checked
    return response.json()


def make_request_with_cache_api(base_url,site_object):
    

    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.

    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
        
    site_object: a site instance
    
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    cache_file=load_cache(CACHE_FILENAME)
    params={'key':MAP_KEY,'origin':site_object.zipcode,'radius':10,'maxMatches':10,
            'ambiguities':'ignore','outFormat':'json'}
 
    
    
    
    if site_object.name in cache_file:
        print('Using cache')
        return cache_file[site_object.name]
    else:
        print("Fetching")
        new_request=make_request_api(base_url,params)
        cache_file[site_object.name]=new_request
        save_cache(cache_file,CACHE_FILENAME)
        return cache_file[site_object.name]


def get_nearby_places(site_object):
    
    base_url='http://www.mapquestapi.com/search/v2/radius'
    
    nearby_dict=make_request_with_cache_api(base_url,site_object)
    
    '''Obtain API data from MapQuest API.

    Parameters
    ----------
    site_object: object
        an instance of a national site

    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    #print(nearby_dict)
    return nearby_dict

def make_nearby_instance_list(nearby_dict):
    '''
    make the nearby dictionary into instance
    
    Parameter:
    ------------
    nearby_dict: a dictionary contain the nearby information
    
    Return:
    -----------
    list of nearby place instances
    '''
    nearby_instance_list=[]
    for member in nearby_dict['searchResults']:
        
    
        nearby_name=member['name']
        
        try:
            nearby_category=member['fields']["group_sic_code_name"].strip()
            if nearby_category=='':
                nearby_category='no category'
            
        except:
            nearby_category=member['fields']["group_sic_code_name_ext"].strip()

        
        try:
            nearby_street_address=member['fields']['address'].strip()
            if nearby_street_address=='':
                nearby_street_address='no street address'
        except:
            nearby_street_address='no street address'
            
        try:
            nearby_city_name=member['fields']['city'].strip()
            if nearby_city_name=='':
                nearby_city_name='no city'      
        except:
            nearby_city_name='no city'
        
        nearby_instance=Nearbyplace(nearby_name,nearby_category,nearby_street_address,nearby_city_name)
        nearby_instance_list.append(nearby_instance)
        
    return nearby_instance_list




if __name__ == "__main__":
    
    base_url='https://www.nps.gov'
    x=0
    while True:

        state=input('enter the full name of a state, eg "california", or enter the abbreviation of a state. eg "CA", or enter exit to quit:').lower()

        if len(state)==2 and state in states.values():
            state_url=base_url+'/'+state+'/'+'/index.htm'
        elif state == 'exit':
            break
        elif state in states.keys():
            state_url=base_url+'/'+states[state]+'/'+'/index.htm'
        else:
            print('invalid input, please reentry the state name')
            continue
        sites_list=get_sites_for_state(state_url)
        
        if len(state)!=2:
            print("List of national sites in", state.upper())
            print('-'*20)
        if len(state)==2:
            print("List of national sites in", get_key(states,state).upper())
            print('-'*20)
                
        i=1
        
        while i<=len(sites_list):
            for site in sites_list:
                print('[',i,'] ',site.info())
                i+=1
        
        while True:
            
            nearby_instance_list=[]
            option=input('enter a number to get the information of nearby places, enter "back" to go back, and enter "exit" to quit:').lower()
            
            
            #print(sites_list[option].url,'This is url')
            if option=="back":
                break
                            
                                            
            if option=="exit": 
                x=1
                break
            elif option.isnumeric():
                if int(option)<=len(sites_list) and option.isnumeric():
                    park_instance=get_site_instance(sites_list[int(option)-1].url)
                    site_name=park_instance.name
                    nearbyplace=get_nearby_places(park_instance)# this is the dictionary
                    #print(nearbyplace,'this is nearby place')
                    nearby_instance_list=make_nearby_instance_list(nearbyplace)
                    print('Places near',site_name.strip())
                    print('-'*20)
                    for nearby_place in nearby_instance_list:
                        print(nearby_place.info())
                    continue
                else:
                    print("invalid input,please retry")
            else:
                print("invalid input,please retry")
                continue
        if x==1:
            break
            


