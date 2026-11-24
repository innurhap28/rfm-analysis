(100000, 5)
(1371980, 7)
(105542, 25)
        t_dat  ...  sales_channel_id
0  2018-09-20  ...                 2
1  2018-09-20  ...                 2
2  2018-09-20  ...                 2
3  2018-09-20  ...                 2
4  2018-09-20  ...                 2

[5 rows x 5 columns]
                                         customer_id  ...                                        postal_code
0  00000dbacae5abe5e23885899a1fa44253a17956c6d1c3...  ...  52043ee2162cf5aa7ee79974281641c6f11a68d276429a...
1  0000423b00ade91418cceaf3b26c6af3dd342b51fd051e...  ...  2973abc54daa8a5f8ccfe9362140c63247c5eee03f1d93...
2  000058a12d5b43e67d225668fa1f8d618c13dc232df0ca...  ...  64f17e6a330a85798e4998f62d0930d14db8db1c054af6...
3  00005ca1c9ed5f5146b52ac8639a40ca9d57aeff4d1bd2...  ...  5d36574f52495e81f019b680c843c443bd343d5ca5b1c2...
4  00006413d8573cd20ed7128e53b7b13819fe5cfc2d801f...  ...  25fa5ddee9aac01b35208d01736e57942317d756b32ddd...

[5 rows x 7 columns]
   article_id  ...                                        detail_desc
0   108775015  ...            Jersey top with narrow shoulder straps.
1   108775044  ...            Jersey top with narrow shoulder straps.
2   108775051  ...            Jersey top with narrow shoulder straps.
3   110065001  ...  Microfibre T-shirt bra with underwired, moulde...
4   110065002  ...  Microfibre T-shirt bra with underwired, moulde...

[5 rows x 25 columns]
<class 'pandas.DataFrame'>
RangeIndex: 100000 entries, 0 to 99999
Data columns (total 5 columns):
 #   Column            Non-Null Count   Dtype  
---  ------            --------------   -----  
 0   t_dat             100000 non-null  str    
 1   customer_id       100000 non-null  str    
 2   article_id        100000 non-null  int64  
 3   price             100000 non-null  float64
 4   sales_channel_id  100000 non-null  int64  
dtypes: float64(1), int64(2), str(2)
memory usage: 3.8 MB
<class 'pandas.DataFrame'>
RangeIndex: 1371980 entries, 0 to 1371979
Data columns (total 7 columns):
 #   Column                  Non-Null Count    Dtype  
---  ------                  --------------    -----  
 0   customer_id             1371980 non-null  str    
 1   FN                      476930 non-null   float64
 2   Active                  464404 non-null   float64
 3   club_member_status      1365918 non-null  str    
 4   fashion_news_frequency  1355969 non-null  str    
 5   age                     1356119 non-null  float64
 6   postal_code             1371980 non-null  str    
dtypes: float64(3), str(4)
memory usage: 73.3 MB
<class 'pandas.DataFrame'>
RangeIndex: 105542 entries, 0 to 105541
Data columns (total 25 columns):
 #   Column                        Non-Null Count   Dtype
---  ------                        --------------   -----
 0   article_id                    105542 non-null  int64
 1   product_code                  105542 non-null  int64
 2   prod_name                     105542 non-null  str  
 3   product_type_no               105542 non-null  int64
 4   product_type_name             105542 non-null  str  
 5   product_group_name            105542 non-null  str  
 6   graphical_appearance_no       105542 non-null  int64
 7   graphical_appearance_name     105542 non-null  str  
 8   colour_group_code             105542 non-null  int64
 9   colour_group_name             105542 non-null  str  
 10  perceived_colour_value_id     105542 non-null  int64
 11  perceived_colour_value_name   105542 non-null  str  
 12  perceived_colour_master_id    105542 non-null  int64
 13  perceived_colour_master_name  105542 non-null  str  
 14  department_no                 105542 non-null  int64
 15  department_name               105542 non-null  str  
 16  index_code                    105542 non-null  str  
 17  index_name                    105542 non-null  str  
 18  index_group_no                105542 non-null  int64
 19  index_group_name              105542 non-null  str  
 20  section_no                    105542 non-null  int64
 21  section_name                  105542 non-null  str  
 22  garment_group_no              105542 non-null  int64
 23  garment_group_name            105542 non-null  str  
 24  detail_desc                   105126 non-null  str  
dtypes: int64(11), str(14)
memory usage: 20.1 MB
         article_id          price  sales_channel_id
count  1.000000e+05  100000.000000     100000.000000
mean   5.892020e+08       0.029593          1.716240
std    1.028513e+08       0.022437          0.450824
min    1.087750e+08       0.000797          1.000000
25%    5.590180e+08       0.016932          1.000000
50%    6.179190e+08       0.025407          2.000000
75%    6.605190e+08       0.033881          2.000000
max    7.299310e+08       0.591525          2.000000
             FN    Active           age
count  476930.0  464404.0  1.356119e+06
mean        1.0       1.0  3.638696e+01
std         0.0       0.0  1.431363e+01
min         1.0       1.0  1.600000e+01
25%         1.0       1.0  2.400000e+01
50%         1.0       1.0  3.200000e+01
75%         1.0       1.0  4.900000e+01
max         1.0       1.0  9.900000e+01
          article_id  ...                        detail_desc
count   1.055420e+05  ...                             105126
unique           NaN  ...                              43404
top              NaN  ...  T-shirt in printed cotton jersey.
freq             NaN  ...                                159
mean    6.984246e+08  ...                                NaN
std     1.284624e+08  ...                                NaN
min     1.087750e+08  ...                                NaN
25%     6.169925e+08  ...                                NaN
50%     7.022130e+08  ...                                NaN
75%     7.967030e+08  ...                                NaN
max     9.594610e+08  ...                                NaN

[11 rows x 25 columns]
                  missing_count  missing_ratio
t_dat                         0            0.0
customer_id                   0            0.0
article_id                    0            0.0
price                         0            0.0
sales_channel_id              0            0.0
                        missing_count  missing_ratio
Active                         907576      66.150819
FN                             895050      65.237831
fashion_news_frequency          16011       1.167000
age                             15861       1.156066
club_member_status               6062       0.441843
customer_id                         0       0.000000
postal_code                         0       0.000000
                              missing_count  missing_ratio
detail_desc                             416       0.394156
perceived_colour_master_name              0       0.000000
garment_group_name                        0       0.000000
garment_group_no                          0       0.000000
section_name                              0       0.000000
section_no                                0       0.000000
index_group_name                          0       0.000000
index_group_no                            0       0.000000
index_name                                0       0.000000
index_code                                0       0.000000
department_name                           0       0.000000
department_no                             0       0.000000
article_id                                0       0.000000
product_code                              0       0.000000
perceived_colour_value_name               0       0.000000
perceived_colour_value_id                 0       0.000000
colour_group_name                         0       0.000000
colour_group_code                         0       0.000000
graphical_appearance_name                 0       0.000000
graphical_appearance_no                   0       0.000000
product_group_name                        0       0.000000
product_type_name                         0       0.000000
product_type_no                           0       0.000000
prod_name                                 0       0.000000
perceived_colour_master_id                0       0.000000
