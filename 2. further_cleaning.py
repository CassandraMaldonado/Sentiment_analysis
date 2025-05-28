# In Dept Cleaning 
# Once I saved the basic cleaning I realized there was still noice in my data, so I tried to replicate webscrapping through this code.

import os
import re
import pickle
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import html


cache_dir = "cache"
input_file = os.path.join(cache_dir, "trafilatura_quality_data.pkl")
output_file = os.path.join(cache_dir, "best_quality_data.pkl")

# I removed navigation elements, dates and additional content to more closely match the Trafilatura quality.
def further_clean_text(text):
    if not text or pd.isna(text):
        return ""
    
    # Converted to string
    text = str(text)
    
    # Removed common navigation items and non-english patterns.
    
    # Removed navigation patterns.
    text = re.sub(r'(?i)(Home|Menu|Navigation|Search|Login|Sign up|Subscribe|Follow us)\s*[|\-•]', '', text)
    
    # Removed common news site section markers.
    text = re.sub(r'(?i)(News|Sports|Technology|Business|Entertainment|Politics|Opinion|Weather|AIXov XwmSpace|technology|Satellite|Science|US|Tiv tauj|Xov Xwm)\s*[|\-•]', '', text)
    
    # Removed dates in various formats.
    text = re.sub(r'(?i)(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}', '', text)
    text = re.sub(r'(?i)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}', '', text)
    text = re.sub(r'(?i)(Mon|Tue|Wed|Thu|Fri|Sat|Sun)[a-z]*\.?\s+\d{1,2},?\s+\d{4}', '', text)
    text = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '', text)
    
    # Removed bylines and publishing info.
    text = re.sub(r'(?i)By\s+[A-Za-z\s\.]+\s*[,|\-]\s*[A-Za-z\s\.]+', '', text)
    text = re.sub(r'(?i)By\s+[A-Za-z\s\.]+\s*$', '', text)
    text = re.sub(r'(?i)Published\s+\d{1,2}[a-z]{0,2}\s+[A-Za-z]+\s+\d{4}', '', text)
    
    # Removed time specifications.
    text = re.sub(r'(?i)\d{1,2}:\d{2}\s*[ap]\.?m\.?(\s+[A-Za-z]+)?', '', text)
    
    # Removed non-english text patterns.
    text = re.sub(r'(?i)Hla mus rau cov ntsiab lus', '', text)
    text = re.sub(r'(?i)Lub neej hauv nroog', '', text)
    
    # Removed text from social media buttons.
    text = re.sub(r'(?i)(Share|Tweet|Email|Print|Facebook|Twitter|LinkedIn|Pinterest|Instagram|WhatsApp)\s*[|\-•]', '', text)
    
    # Removed copyright notices.
    text = re.sub(r'(?i)©\s*\d{4}.*?(rights reserved|all rights)', '', text)
    text = re.sub(r'(?i)Copyright\s*©?\s*\d{4}.*?$', '', text)
    
    # Removed comment section indicators.
    text = re.sub(r'(?i)(Comments|Leave a comment|Add a comment|Join the conversation)', '', text)
    
    # Cleaned up excessive new lines and spaces by replacing more the 3 new lines with just 2 and more then 2 with just 1.
    text = re.sub(r'\n{3,}', '\n\n', text)  
    text = re.sub(r' {2,}', ' ', text)      
    
    # Removed lines that were too short since those were likely menu items.
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if len(line.strip()) > 15 or line.strip() == '']
    text = '\n'.join(cleaned_lines)
    
    # Final cleanup of whitespaces.
    text = text.strip()
    
    return text


# Cleaned to extract only the main article text by removing navigation, UI elements, boilerplate and other non-article content.

def enhanced_clean_text(text):
    if not text or pd.isna(text):
        return ""
    
    # Converted to string.
    text = str(text)

    # Removed navigation elements.
    text = re.sub(r'(?i)(Home|Menu|Navigate|Search|Top|Back to top|Skip to( main)? content|Sign in|Log in|Register|Subscribe|Follow)(\s+[|•>\-→]|\s*$)', '', text)
    text = re.sub(r'(?i)(Main Menu|Navigation Menu|Site Navigation|Primary Menu|Secondary Menu)', '', text)
    text = re.sub(r'(?i)(Header|Footer|Sidebar|Widget|Column|Panel|Section|Module|Block)', '', text)
    text = re.sub(r'(?i)breadcrumb[s]?', '', text)
    
    # Removed previous or next article navigation.
    text = re.sub(r'(?i)Previous\s*[:\-]?\s*[^.\n]+', '', text)
    text = re.sub(r'(?i)Next\s*[:\-]?\s*[^.\n]+', '', text)
    text = re.sub(r'(?i)(Previous|Earlier|Next|Later)\s+(Article|Post|Story|Read|Page)', '', text)
    text = re.sub(r'(?i)(Read|See)\s+(Previous|Next|More|Related|Also)', '', text)
    
    # Removed the section headers appearing in most websites.
    text = re.sub(r'(?i)(News|Sports|Technology|Business|Entertainment|Politics|Opinion|Weather|' +
                  r'World|Local|Regional|National|International|Breaking|Latest|Top Stories|' +
                  r'Trending|Features|Analysis|Commentary|Videos|Photos|Premium|Special|Exclusive)', '', text)
    
    # Removed network and portal sections.
    text = re.sub(r'(?i)Our\s+Network\s+Portals?.*?(?=\n\n|\Z)', '', text)
    text = re.sub(r'(?i)(Related|Sister|Partner)\s+(Sites?|Portals?|Networks?|Channels?|Publications?)', '', text)
    text = re.sub(r'(?i)(More|Other)\s+(From|By|On|At)\s+[A-Za-z\s]+', '', text)
    
    # Removed common footer elements.
    text = re.sub(r'(?i)(Contact Us|About Us|Our Team|Careers|Jobs|Sitemap|FAQ|Help|Support)', '', text)
    text = re.sub(r'(?i)(Terms of Service|Privacy Policy|Cookie Policy|User Agreement)', '', text)
    text = re.sub(r'(?i)(Follow Us|Connect with Us|Find Us|Join Us) on Social Media', '', text)
    
    # Removed footer taglines and slogans.
    text = re.sub(r'(?i)(All|Get)\s+the\s+(latest|best|top|breaking)\s+(news|stories|content|updates)', '', text)
    text = re.sub(r'(?i)Stay\s+(tuned|updated|informed|connected)', '', text)
    text = re.sub(r'(?i)Thanks\s+for\s+(reading|visiting|subscribing)', '', text)
    
    # Removed date formats.
    text = re.sub(r'(?i)(Posted|Published|Updated|Modified|Date):?\s*', '', text)
    text = re.sub(r'(?i)\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', '', text)
    text = re.sub(r'(?i)(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2}(st|nd|rd|th)?,\s+\d{4}', '', text)
    text = re.sub(r'(?i)(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?\s+\d{1,2}(st|nd|rd|th)?,?\s+\d{4}', '', text)
    text = re.sub(r'(?i)(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|Mon|Tue|Wed|Thu|Fri|Sat|Sun),?\s+\d{1,2}\s+\w+\s+\d{4}', '', text)
    text = re.sub(r'\d{1,2}/\d{1,2}/\d{2,4}', '', text)
    text = re.sub(r'\d{4}-\d{2}-\d{2}', '', text)
    
    # Removed time formats.
    text = re.sub(r'\d{1,2}:\d{2}(:\d{2})?\s*(am|pm|AM|PM|a\.m\.|p\.m\.)', '', text)
    text = re.sub(r'(?i)(EDT|EST|CDT|CST|MDT|MST|PDT|PST|UTC|GMT)(\s+|$)', '', text)
    
    # Removed author info and bylines.
    text = re.sub(r'(?i)By\s+[A-Za-z\s\.\-]+\s*[,|\-]\s*[A-Za-z\s\.\-]+', '', text)
    text = re.sub(r'(?i)By\s+[A-Za-z\s\.\-]+\s*(Staff|Reporter|Editor|Writer|Correspondent|Contributor)', '', text)
    text = re.sub(r'(?i)(Written|Reported)\s+by\s+[A-Za-z\s\.\-]+', '', text)
    text = re.sub(r'(?i)Author[:]?\s+[A-Za-z\s\.\-]+', '', text)
    text = re.sub(r'(?i)(Staff|Special)\s+(Writer|Reporter|Correspondent)', '', text)
    
    # Removed social media.
    text = re.sub(r'(?i)(Share|Tweet|Post|Email|Print|Copy|Save|Bookmark|Favorite|Like|Follow|Subscribe|Connect)(\s+on|\s+to|\s+via|\s+with)?\s+' +
                  r'(Facebook|Twitter|Instagram|LinkedIn|Pinterest|Reddit|Tumblr|WhatsApp|Telegram|YouTube|TikTok|Snapchat|Email|Print)', '', text)
    text = re.sub(r'(?i)(Follow|Like|Subscribe to) us on', '', text)
    text = re.sub(r'(?i)(Follow|Connect with) us', '', text)
    text = re.sub(r'(?i)Share this (article|post|story)', '', text)
    text = re.sub(r'(?i)Share on social (media|networks)', '', text)
    
    # Removed social media follow sections.
    text = re.sub(r'(?i)(Follow|Connect|Find|Join)\s+(Us|with\s+Us|Me)\s+(on|at)\s+(Social\s+Media|Facebook|Twitter|Instagram|LinkedIn)', '', text)
    text = re.sub(r'(?i)Please\s+follow\s+us\s+on\s+Social\s+Media', '', text)
    text = re.sub(r'(?i)Follow\s+(on|us\s+on)\s+(Facebook|Twitter|Instagram|LinkedIn|YouTube|TikTok|Pinterest)', '', text)
    
    # Removed comment sections.
    text = re.sub(r'(?i)(Comments|Leave a comment|Add a comment|Join the conversation|Discussion|Reply|Replies)', '', text)
    text = re.sub(r'(?i)\d+ comments?', '', text)
    text = re.sub(r'(?i)(Most popular|Top|Best) comments', '', text)
    
    # Removed cookies notices and privacy popups.
    text = re.sub(r'(?i)(Cookie|Privacy|Consent|GDPR|Data protection)(\s+Notice|\s+Policy|\s+Preferences|\s+Settings)', '', text)
    text = re.sub(r'(?i)We use cookies', '', text)
    text = re.sub(r'(?i)This (website|site) uses cookies', '', text)
    text = re.sub(r'(?i)By (continuing|browsing|using) (this|our) (site|website)', '', text)
    text = re.sub(r'(?i)Accept( all| cookies| terms| conditions)?', '', text)
    
    # Removed copyright. 
    text = re.sub(r'(?i)©\s*\d{4}.*?(rights reserved|all rights)', '', text)
    text = re.sub(r'(?i)Copyright\s*©?\s*\d{4}.*?$', '', text)
    text = re.sub(r'(?i)All rights reserved', '', text)
    text = re.sub(r'(?i)Terms (of|and) (Use|Service|Privacy)', '', text)
    
    # Removed ads text. 
    text = re.sub(r'(?i)(Advertisement|Sponsored|Promotion|Ad|Ads|Advert)', '', text)
    text = re.sub(r'(?i)(Special|Promoted|Featured|Sponsored) Content', '', text)
    text = re.sub(r'(?i)From our sponsors?', '', text)
    text = re.sub(r'(?i)Recommended for you', '', text)
    
    # Removed UI related elements.
    text = re.sub(r'(?i)(Click|Tap) (here|to|on)', '', text)
    text = re.sub(r'(?i)(Read|See|View|Learn) (more|all|full|article)', '', text)
    text = re.sub(r'(?i)(Next|Previous|Continue reading|More stories)', '', text)
    text = re.sub(r'(?i)(Load|Show) more', '', text)
    text = re.sub(r'(?i)(Sign up|Subscribe) (now|today|for|to our)', '', text)
    
    # Removed analytics and tracking.
    text = re.sub(r'(?i)(Tracking ID|Analytics|Pixel|Tag|UA-\d+-\d+)', '', text)
    text = re.sub(r'(?i)(Google Analytics|Google Tag Manager|Facebook Pixel)', '', text)
    
    # Removed contact info. 
    text = re.sub(r'(?i)Contact\s+(Us|Information|Details).*?(?=\n\n|\Z)', '', text)
    text = re.sub(r'(?i)(Email|Phone|WhatsApp|Telephone|Mobile|Fax)(\s+Us)?(\s+at)?:?.*?(?=\n|\Z)', '', text)
    text = re.sub(r'(?i)(Our|Company|Corporate|Business|Editorial)\s+(Address|Office|Headquarters)', '', text)
    
    # Removed email addresses and phone numbers in footer.
    text = re.sub(r'(?i)([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)(\s*\.\s*)?$', '', text)
    text = re.sub(r'(?i)WhatsApp\s+Voice:\s*[\+]?[\d\-\s]+', '', text)
    text = re.sub(r'(?i)Phone\s*:?\s*[\+]?[\d\-\s]+', '', text)
    text = re.sub(r'(?i)Call\s+Us\s*(at|on)?\s*:?\s*[\+]?[\d\-\s]+', '', text)
    
    # Removed HTML,CSS or JS fragments.
    text = re.sub(r'</?[a-z]+[^>]*>', '', text)  
    text = re.sub(r'\{\{.*?\}\}', '', text)      
    text = re.sub(r'\$\(.*?\)', '', text)        
    text = re.sub(r'function\s*\(.*?\)', '', text) 
    text = re.sub(r'#[a-zA-Z][\w-]*\s*\{[^}]*\}', '', text) 
    
    # Removed urls and website references.
    text = re.sub(r'(?i)(Visit|Check)?\s+Our\s+Website:?\s*', '', text)
    text = re.sub(r'(?i)www\.[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/[^\s]*)?', '', text)
    text = re.sub(r'https?://[^\s]+', '', text)
    text = re.sub(r'(?i)[A-Za-z]+\.(com|org|net|edu|io|ai|co|us|info|news|media)(\s+|$)', '', text)
    
    # Removed website elements.
    text = re.sub(r'(?i)(Username|Password|Email|Name|First name|Last name|Address|Phone|Submit|Cancel)', '', text)
    text = re.sub(r'(?i)(Login|Logout|Sign in|Sign out|Register|Create account)', '', text)
    text = re.sub(r'(?i)(Search|Filter|Sort by|Order by)', '', text)
    
    # Removed pages info.
    text = re.sub(r'(?i)Page \d+ of \d+', '', text)
    text = re.sub(r'(?i)Pages?: \d+(-|–)\d+', '', text)
    text = re.sub(r'(?i)Results? \d+-\d+ of \d+', '', text)
    
    # Removed extra section indicators.
    text = re.sub(r'(?i)(Also Read|Related|Similar|More Like This|You May Also Like|Recommended|Popular|Trending)', '', text)
    text = re.sub(r'(?i)(Top|Latest) (Stories|News|Articles)', '', text)
    text = re.sub(r'(?i)(Editor\'s|Our) Picks?', '', text)
    
    # Removed tags and categories.
    text = re.sub(r'(?i)Tags?: .*?(?=\n|$)', '', text)
    text = re.sub(r'(?i)Categories?: .*?(?=\n|$)', '', text)
    text = re.sub(r'(?i)Keywords?: .*?(?=\n|$)', '', text)
    
    # Removed excessive whitespaces.
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'\t+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Removed lines that are too short since they were likely navigation buttons.
    lines = text.split('\n')
    cleaned_lines = [line for line in lines if len(line.strip()) > 15 or line.strip() == '']
    text = '\n'.join(cleaned_lines)
    
    # Removed lines that were likely headlines repeated within the article,
    lines = text.split('\n')
    title_pattern = r'^[A-Z][^.!?]*[.!?]$'
    non_title_lines = []
    seen_titles = set()
    
    for line in lines:
        line_stripped = line.strip()
        if re.match(title_pattern, line_stripped) and len(line_stripped) < 100:
            if line_stripped in seen_titles:
                continue  # Skip duplicate titles
            seen_titles.add(line_stripped)
        non_title_lines.append(line)
    
    text = '\n'.join(non_title_lines)
    
    text = text.strip()
    
    return text

#  Cleaned the title to remove publisher names and noise.
def further_clean_title(title):
    if not title or pd.isna(title):
        return ""
    
    # Convert to string.
    title = str(title)
    
    # Removed common publisher indicators
    patterns = [
        r'\s*\|\s*[^|]+$',                    # | Website
        r'\s*–\s*[^–]+$',                     
        r'\s*-\s*[^-]+\.(com|org|net)$',     
        r'\s*-\s*[A-Za-z\s]+Times$',          
        r'\s*\(\s*[^)]+\s*\)$',               # (Publisher Name)
        r'\s*\|\s*[A-Za-z0-9\s\.]+$',         # | Website Name
        r'\s*-\s*[A-Za-z0-9\s\.]+$',          # - Website Name
        r'\s*—\s*[A-Za-z0-9\s\.]+$',          # — Website Name
        r'\s*:\s*[A-Za-z0-9\s\.]+\.(com|org|net|edu)$', # : website.com
        r'\s*[·•]\s*[A-Za-z0-9\s\.]+$',       # · Website Name
    ]
    
    for pattern in patterns:
        title = re.sub(pattern, '', title)
    
    # Removed quotation marks.
    title = re.sub(r'^"(.*)"$', r'\1', title)
    title = re.sub(r'^\'(.*)\'$', r'\1', title)
    
    # Clean up any remaining special characters and whitespaces.
    title = title.strip()
    
    return title

# More in depth cleaning of article titles.
def enhanced_clean_title(title):
    if not title or pd.isna(title):
        return ""
    
    title = str(title)
    
    # Removed common publisher indicators with more patterns.
    patterns = [
        r'\s*\|\s*[^|]+$',                      # | Publisher Name
        r'\s*–\s*[^–]+$',                       # – Publisher Name
        r'\s*-\s*[^-]+\.(com|org|net|edu|io|co|ai|app)$',  # - website.com
        r'\s*-\s*[A-Za-z\s]+Times$',            # - Some Times
        r'\s*-\s*[A-Za-z\s]+News$',             # - Some News
        r'\s*-\s*[A-Za-z\s]+Post$',             # - Some Post
        r'\s*\(\s*[^)]+\s*\)$',                 # (Publisher Name)
        r'\s*»\s*[^»]+$',                       # » Publisher Name
        r'\s*:\s*[A-Za-z0-9\s\.]+\.(com|org|net|edu|io|co|ai|app)$',  # : website.com
        r'\s*[·•]\s*[A-Za-z0-9\s\.]+$',         # · Website Name
        r'^\[\s*[^\]]+\s*\]\s*',                
        r'\s*\[[^\]]+\]$',                      
        r'^\d{1,2}/\d{1,2}(/\d{2,4})?\s*:?\s*', # Date: Title
        r'^\d{1,2}-\d{1,2}(-\d{2,4})?\s*:?\s*', # Date: Title
        r'^\d{4}-\d{2}-\d{2}\s*:?\s*',          # Date: Title
    ]
    
    for pattern in patterns:
        title = re.sub(pattern, '', title)
    
    # Removed common prefixes.
    prefixes = [
        r'^(BREAKING|EXCLUSIVE|UPDATE|WATCH|VIDEO|PHOTOS?|PICTURED|REVEALED|UPDATED):?\s+',
        r'^(LIVE|LATEST|JUST IN|DEVELOPING|TRENDING):?\s+',
        r'^(OPINION|ANALYSIS|COMMENTARY|REVIEW|EDITORIAL):?\s+',
        r'^(FACT CHECK|FACT SHEET|Q&A|FAQ|HOW TO|GUIDE):?\s+',
        r'^(OFFICIAL|CONFIRMED|LEAKED|RUMOR):?\s+',
    ]
    
    for prefix in prefixes:
        title = re.sub(prefix, '', title, flags=re.IGNORECASE)
    
    # Removed quotation marks that might remain from previous cleaning.
    title = re.sub(r'^["\'](.*)["\']$', r'\1', title)
    
    # Removed excessive spaces.
    title = re.sub(r'\s+', ' ', title)
    
    # Cleaned up any remaining special characters and whitespaces.
    title = title.strip()
    
    return title

# Here I loaded my previously cleaned data and applied further cleaning.
def process_cleaned_dataset():
    # Checked if the input file existed.
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found. Make sure you've run your original cleaning script first.")
        return None
    
    # Loaded the dataset.
    print(f"Loading cached dataset from {input_file}...")
    try:
        with open(input_file, 'rb') as f:
            df = pickle.load(f)
        print(f"Dataset loaded successfully. Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None
    
    # Using a copy to preserve the original.
    df_clean = df.copy()
    
    # Applied extra cleaning to text.
    print("Extra cleaning.")
    if 'cleaned_text' in df_clean.columns:
        df_clean['trafilatura_text'] = df_clean['cleaned_text'].apply(further_clean_text)
    else:
        print("Warning: 'cleaned_text' column not found. Looking for 'text' column instead.")
        if 'text' in df_clean.columns:
            df_clean['trafilatura_text'] = df_clean['text'].apply(further_clean_text)
        else:
            print("Error: Neither 'cleaned_text' nor 'text' column found.")
            return None
    
    # Applied extra cleaning to the title.
    print("Applying further title cleaning...")
    if 'title' in df_clean.columns:
        df_clean['trafilatura_title'] = df_clean['title'].apply(further_clean_title)
    else:
        print("Warning: 'title' column not found.")
        df_clean['trafilatura_title'] = ["Unknown Title" for _ in range(len(df_clean))]
    
    # Saved the new cleaned dataset.
    print(f"Saving further cleaned dataset to {output_file}...")
    with open(output_file, 'wb') as f:
        pickle.dump(df_clean, f)
    print(f"Dataset saved successfully.")
    
    # Saved a minimal version with just the essential columns.
    minimal_cols = ['trafilatura_title', 'trafilatura_text']
    if 'date' in df_clean.columns:
        minimal_cols.append('date')
    if 'year' in df_clean.columns:
        minimal_cols.append('year')
    if 'month' in df_clean.columns:
        minimal_cols.append('month')
    if 'yearmonth' in df_clean.columns:
        minimal_cols.append('yearmonth')
    if 'source_domain' in df_clean.columns:
        minimal_cols.append('source_domain')
    
    minimal_file = os.path.join(cache_dir, "trafilatura_quality_minimal.pkl")
    df_minimal = df_clean[minimal_cols].copy()
    
    with open(minimal_file, 'wb') as f:
        pickle.dump(df_minimal, f)
    print(f"Minimal dataset saved to {minimal_file}")
    
    # Checked the first rows.
    return df_clean[['trafilatura_title', 'trafilatura_text']].head()

# Analyzed the differences between the original and latest cleaned text.
def analyze_cleaning_differences(df_sample=5):
    try:
        with open(input_file, 'rb') as f:
            df = pickle.load(f)
        
        with open(output_file, 'rb') as f:
            df_clean = pickle.load(f)
        
        # Selected the columns for comparison.
        title_cols = ['title', 'trafilatura_title'] if 'title' in df.columns else ['trafilatura_title']
        text_cols = ['cleaned_text', 'trafilatura_text'] if 'cleaned_text' in df.columns else ['trafilatura_text']
        
        # Random sample.
        sample_idx = df.sample(df_sample).index
        
        print("\n" + "="*80)
        print("Comparing title cleaning.")
        print("="*80)
        
        for idx in sample_idx:
            if len(title_cols) > 1:
                print(f"\nOriginal title: {df.loc[idx, title_cols[0]]}")
                print(f"Cleaned title:  {df_clean.loc[idx, title_cols[1]]}")
            else:
                print(f"\nCleaned title:  {df_clean.loc[idx, title_cols[0]]}")
            print("-"*80)
        
        print("\n" + "="*80)
        print("Comparing text cleaning.")
        print("="*80)
        
        for idx in sample_idx:
            if len(text_cols) > 1:
                orig_text = df.loc[idx, text_cols[0]]
                clean_text = df_clean.loc[idx, text_cols[1]]
                
                print(f"\nOriginal text (first 200 chars):")
                print(f"{orig_text[:200]}..." if len(orig_text) > 200 else orig_text)
                
                print(f"\nCleaned text (first 200 chars):")
                print(f"{clean_text[:200]}..." if len(clean_text) > 200 else clean_text)
                
                # Calculate character reduction percentage
                orig_len = len(orig_text)
                clean_len = len(clean_text)
                reduction = ((orig_len - clean_len) / orig_len) * 100 if orig_len > 0 else 0
                
                print(f"\nCharacter count: {orig_len} → {clean_len} ({reduction:.1f}% reduction)")
            else:
                clean_text = df_clean.loc[idx, text_cols[0]]
                print(f"\nCleaned text (first 200 chars):")
                print(f"{clean_text[:200]}..." if len(clean_text) > 200 else clean_text)
            
            print("-"*80)
        
        return True
    except Exception as e:
        print(f"Error analyzing cleaning differences: {e}")
        return False

# Processed the dataset.
if __name__ == "__main__":
    result = process_cleaned_dataset()
    
    if result is not None:
        print("\nSample of the cleaned data:")
        print(result)
        
        # Analyzed differences.
        analyze_cleaning_differences()
        
        print("\n Extra cleaning done.")
        print(f"The cleaned data is saved at: {output_file}")
        print(f"A minimal version is saved at: {os.path.join(cache_dir, 'trafilatura_quality_minimal.pkl')}")
