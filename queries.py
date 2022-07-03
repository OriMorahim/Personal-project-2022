FETCH_DATASET_FLAT = '''
WITH engagments AS (
  SELECT
    *,

    # bining date parts
    CASE 
      WHEN hour_of_day BETWEEN 8 AND 18 THEN 1 
      ELSE 0 END AS is_working_hours,
    CASE 
      WHEN hour_of_day BETWEEN 6 AND 9 THEN 'early_moning' 
      WHEN hour_of_day BETWEEN 10 AND 13 THEN 'late_moning'
      WHEN hour_of_day BETWEEN 14 AND 17 THEN 'noon'
      WHEN hour_of_day BETWEEN 18 AND 21 THEN 'early_evening'
      WHEN hour_of_day BETWEEN 22 AND 24 THEN 'late_evening'
      ELSE 'night' END part_of_day,
    CASE 
      WHEN hour_of_day BETWEEN 6 AND 9 THEN 0 
      WHEN hour_of_day BETWEEN 10 AND 13 THEN 1
      WHEN hour_of_day BETWEEN 14 AND 17 THEN 2
      WHEN hour_of_day BETWEEN 18 AND 21 THEN 3
      WHEN hour_of_day BETWEEN 22 AND 24 THEN 4
      ELSE 5 END part_of_day_ordianl,
    CASE 
      WHEN 
        day_of_week NOT IN (7,1) THEN 1
        ELSE 0 END AS is_working_day,
    CASE 
      WHEN day_of_week IN (2,3,4) THEN 'begining'
      WHEN day_of_week IN (5,6) THEN 'middle'
      ELSE 'end' END AS part_of_week,
    CASE 
      WHEN day_of_week IN (2,3,4) THEN 0
      WHEN day_of_week IN (5,6) THEN 1
      ELSE 2 END AS part_of_week_ordinal,
    CASE
      WHEN day_of_month <= 10 THEN 'begining'
      WHEN day_of_month <= 20 THEN 'middle'
      ELSE 'end' END AS part_of_month,
    CASE
      WHEN day_of_month <= 10 THEN 0
      WHEN day_of_month <= 20 THEN 1
      ELSE 2 END AS part_of_month_ordinal
  FROM (
    SELECT
      contact_id,
      campaign_id,
      event, -- Supervisor (Y)

      # extract date parts
      EXTRACT(HOUR FROM timestamp) AS hour_of_day,
      EXTRACT(DAYOFWEEK FROM timestamp) AS day_of_week,
      EXTRACT(DAY FROM timestamp) aS day_of_month,

      # proxy to y
      CASE WHEN event IN ('open', 'click', 'reply', 'survey completed') THEN 1 ELSE 0 END AS is_engaged -- Supervisor (Y)
    FROM
      `rb_rawdata.Engagements`
  )
),

contacts_and_companies AS (
  SELECT
    contact.contact_id,
    contact.company_id,
    contact.seniority,
    contact.function,
    contact.country,
    contact.state,

    # extract features from title 
    IFNULL(LENGTH(REGEXP_REPLACE(contact.position, r'[^\s]', '')) + 1, -1) AS words_in_title,
    IFNULL(LENGTH(REGEXP_REPLACE(contact.function, r'[^,]', '')) + 1, -1) AS number_of_functions,
    
    CASE 
      WHEN REGEXP_CONTAINS(contact.seniority, r'(C\wO|CHRO|CISO|Officer|President|VP)') THEN 'very_high'
      WHEN REGEXP_CONTAINS(contact.seniority, r'(Head|Director)') THEN 'high'
      WHEN REGEXP_CONTAINS(contact.seniority, r'(Manager|Lead)') THEN 'medium'
      WHEN REGEXP_CONTAINS(contact.seniority, r'(Assistant|Non-Management|Junior|Senior)') THEN 'low'
      ELSE 'unknown' END AS managment_level,

    # company related featuers
    REPLACE(REPLACE(company.size, '-', '_'),',','') AS company_size,
    company.linkedin_industry
    
  FROM
    `rb_rawdata.Contacts` AS contact LEFT JOIN `rb_rawdata.Companies` AS company
    ON
      contact.company_id = company.company_id
)


SELECT 
  eng.*,
  cont.* EXCEPT(contact_id, function)
FROM
  engagments  AS eng LEFT JOIN contacts_and_companies AS cont
  ON
    eng.contact_id = cont.contact_id 
'''