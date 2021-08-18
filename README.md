# covid19-world-vaccination-progress
Overview: TETLT -> Data Visualisation -> Data Modelling

Tools Used: Microsoft Excel, Microsoft Visual Studio, Microsoft SQL Server, Tableau, PyCharm

Packages Used in Data Modelling: pyodbc, numpy, pandas, scikit-learn, matplotlib

This project is basically an extension to my learning from the udemy course. I thought of going through the BASIC journey of a Data Scientist (involving data extraction, data wrangling, data visualisation and data modelling). I chose a dataset which involved the world vaccination progress from Covid-19 virus till July 28, 2021.

Summary of the Project:

With the dataset achieved in the '.csv' format, I followed the blueprint and converted the file into a '.txt' format and used the Text Query Editor in Microsoft Excel to import the file and the first transformation of the data was taken place there. Then the file was changed into a .csv format and uploaded in visual Studio where using Control Flows, Data Flows (Flat File source for import, OLE DB for export and Conditional Split to remove bad records from good records) was taken place. QA checks were constantly perfomred during each step of this process i.e. while importing and using conditional splits. With the export into Microsoft SQL Server, (be sure that the relational schema is still in the RAW format), I used stored procedures in order to convert the RAW table into a proper Working Table (WRK Table) with the data types as expected for each of the entities. I used Stored Procedures and not just normal SQL Query Page because my target was not to save the it in the local directory but on the Server, plus I wanted the query to be executed ona  single call (added advantage), which reduces network traffic and improves round-trip response time. During this process several QA checks were performed again to make sure the data was proper and ready to be used  and to get rid of all the errors (truncation and validation, to name a few).

Following that, I used Tableau to perform data visualisation on the preprocessed and clean dataset. Various hypothesis were perfomed as shown in one of the NOtepad++ files attached and various visualisations were created to be able to create an insightful dashboard showing the countries vaccinated in the world and the timeline from when the numbers started incraesing till July 28, this year. This dashboard is available at the below attached Tableau public link. 

Again with the dataset obtained in SQL Server, I used Python to model the data using Linear Regression (knowing the data was really small and not worthy to be modelled and had no predictors whatsoever, I still tried to model it to make sure that this assumption was correct and not all datasets can be passed for this step). So, the first step I did was to integrate Python with Microsoft SQL Server using 'pyodbc' package. Once the data was available in the dataframe, I used numpy for basic mathematical operations, pandas for data analysis and preprocessing, matplotlib for data visualisation and scikit-learn for data modelling). Following the feature extraction and data cleaning, it was found that none of the predictors were related with the response variable to an extent that they could be used for modelling, and using Linear Regression and calculating the RMSE and ADJUSTED-R SQUARED value (which was poor), the assumption was verified. 

Tableau public Link: https://public.tableau.com/views/CovidVaccinationsWorldProgress/CovidVaccinesProgress?:language=en-US&:display_count=n&:origin=viz_share_link
