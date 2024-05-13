from scrape import scrape_posts
from init import start
import pandas as pd
import prawcore

relevant_subreddits = ['AVXL', 'HOOKIPA', 'ClinTrialExplain', 'researchclinics', 'MCRB', 'PTGX', 'LCTX', 'RVPH', 'PRVB', 'BCDA', 'T1dResearch', 'OYST', 'sellasLifescience', 'VRPX', 'TriallEcosystem', 'AFMD', 'LXRX', 'medscape', 'ModernClinicalTrials', 'JNCE', 'MREO', 'journalclub', 'RVNC', 'MIRM', 'CERE', 'clinicalresearch', 'ADGI', 'CloudDX', 'PubMedTrending', 'PatientEngagement', 'FULC', 'clinicaltrials', 'BBIO', 'Statistics_help_', 'ClinTexCTi', 'ATXI', 'clinicaltrialsunit', 'BONS', 'survodutide', 'ketoscience', 'harmreduction']
df_list = []

for subreddit_name in relevant_subreddits:
    try:
        reddit = start()
        df = scrape_posts(reddit, subreddit_name)
        df_list.append(df)
    except prawcore.exceptions.TooManyRequests:
        print("Rate limit exceeded. Exiting loop.")
        break

final_df = pd.concat(df_list)
final_df.to_csv('clinical_trial_data.csv', index=False)