import json

# Arun Jaitley Stadium, Delhi
# Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow
# Eden Gardens, Kolkata
# Himachal Pradesh Cricket Association Stadium, Dharamsala
# M Chinnaswamy Stadium, Bengaluru
# MA Chidambaram Stadium, Chennai
# Narendra Modi Stadium, Ahmedabad
# Punjab Cricket Association IS Bindra Stadium, Mohali
# Rajiv Gandhi International Stadium, Hyderabad
# Sawai Mansingh Stadium, Jaipur
# Wankhede Stadium, Mumbai

venue_mapping = {
    'Arun Jaitley Stadium': {
        'aliases': ['Arun Jaitley Stadium, Delhi', 'Feroz Shah Kotla'],
        'tags': ['Delhi', 'Arun Jaitley'],
    },

    'Barsapara Cricket Stadium': {
        'aliases': ['Barsapara Cricket Stadium, Guwahati'],
        'tags': [
            'Guwahati',
            'Barsapara',
            'Bhupen Hazarika',
            'Assam Cricket Association Stadium',
        ],
    },

    'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium': {
        'aliases': [
            'Bharat Ratna Shri Atal Bihari Vajpayee Ekana Cricket Stadium, Lucknow',
        ],
        'tags': ['Lucknow', 'Ekana', 'Atal Bihari'],
    },

    'Eden Gardens': {
        'aliases': ['Eden Gardens, Kolkata'],
        'tags': ['Kolkata', 'Eden Gardens'],
    },

    'Himachal Pradesh Cricket Association Stadium': {
        'aliases': ['Himachal Pradesh Cricket Association Stadium, Dharamsala'],
        'tags': ['Dharamsala', 'Himachal Pradesh'],
    },

    'M Chinnaswamy Stadium': {
        'aliases': [
            'M Chinnaswamy Stadium, Bengaluru',
            'M Chinnaswamy Stadium, Bangalore',
            'M.Chinnaswamy Stadium',
            'M.Chinnaswamy Stadium, Bengaluru',
            'M.Chinnaswamy Stadium, Bangalore',
        ],
        'tags': ['Bengaluru', 'Bengalore', 'Chinnaswamy'],
    },

    'MA Chidambaram Stadium': {
        'aliases': [
            'MA Chidambaram Stadium, Chennai',
            'MA Chidambaram Stadium, Chepauk',
            'MA Chidambaram Stadium, Chepauk, Chennai',
        ],
        'tags': ['Chennai', 'Chepauk', 'Chidambaram'],
    },

    'Narendra Modi Stadium': {
        'aliases': ['Narendra Modi Stadium, Ahmedabad'],
        'tags': ['Ahmedabad', 'Narendra Modi'],
    },

    'Punjab Cricket Association IS Bindra Stadium': {
        'aliases': [
            'Punjab Cricket Association IS Bindra Stadium, Mohali',
            'Punjab Cricket Association Stadium, Mohali',
        ],
        'tags': ['Mohali', 'Punjab Cricket Association', 'IS Bindra'],
    },

    'Rajiv Gandhi International Stadium': {
        'aliases': [
            'Rajiv Gandhi International Stadium, Hyderabad',
            'Rajiv Gandhi International Stadium, Uppal',
        ],
        'tags': ['Hyderabad', 'Rajiv Gandhi'],
    },

    'Sawai Mansingh Stadium': {
        'aliases': ['Sawai Mansingh Stadium, Jaipur'],
        'tags': ['Jaipur', 'Sawai Mansingh'],
    },

    'Wankhede Stadium': {
        'aliases': ['Wankhede Stadium, Mumbai'],
        'tags': ['Mumbai', 'Wankhede'],
    },
}


def to_kebab_case(string):
    return '-'.join(
        string.replace(",", "").replace(".", "").split()
    ).lower()


venue_mapping_normal = {}
venue_mapping_kebab = {}
venue_mapping_tags = {}
for key in venue_mapping:
    for venue in [key, *venue_mapping[key]['aliases']]:
        venue_mapping_normal[venue] = key
        venue_mapping_kebab[to_kebab_case(venue)] = key

    for tag in venue_mapping[key]['tags']:
        venue_mapping_tags[tag.lower()] = key

with open('venue_mapping_normal.json', 'w') as f:
    json.dump(venue_mapping_normal, f, indent=2)
with open('venue_mapping_kebab.json', 'w') as f:
    json.dump(venue_mapping_kebab, f, indent=2)
with open('venue_mapping_tags.json', 'w') as f:
    json.dump(venue_mapping_tags, f, indent=2)
