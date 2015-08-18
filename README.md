# CreatePage

Applies Selenium Webdriver to create a Firefox window and automatically create webpages for sharp school sites with a .csv guideline.

Added functionality to grab content from previous school pages and paste into pages created.


## Instructions


1. Download and set-up [CMS Extension](https://github.com/zrlu/CMS-Extension).
2. Set up the .csv file which will be used as a guideline.
  1. Open the Excel sheet given by the client.
  2. Copy the sheet, starting from the row with the first page you would like to be created until the column with the page URL.
  3. Paste the sheet into another Excel file and save it as a .csv file.
  4. Make sure that:
    * there are no blank rows in between pages
    * there is only one page name per line
    * all new pages/blank pages say "New Page" in the Page URL column
  5. Add any further subpages which you would like the program to create (you can add new columns if you require level 4 or further).
  6. All content space pages' names can be left unchanged. For other types of pages, you must add a number in front of the page name. (e.g. 3Files or 4Calendar)
  	* 0 - Content Space
    * 1 - External Link
      * For external links, in front of the Page URL which is being linked to, you must add a number in front to specify what type of link it is. (e.g. 0http://google.ca or 1http://domain.com/file.pdf)
      	* 0 - external link
      	* 1 - internal file
      	* 2 - internal page
    * 2 - Photo Gallery
    * 3 - Document Container
    * 4 - Calendar
    * 5 - Form Page
    * 6 - Discussion - currently not supported
    * 7 - News
    * 8 - Teacher Page
    * 9 - Blog - currently not supported
    * 9 - Wiki
   7. Save the file and move it to the same directory as the program.
3. At the beginning of the program, change the variables as required.

  ```
  # THINGS TO CHANGE:
  csvName = "file.csv"
  startingPage = "http://example.ss8.sharpschool.com/cms/One.aspx?portalId=1110172&pageId=1110180"
  loginPage = "http://example.ss8.sharpschool.com/gateway/Login.aspx?ReturnUrl=%2f"
  divName = "contentContainer"
  ```

  * csvName: the name of the .csv file which you prepared earlier
  * startingPage: the SharpSchool URL which you would like the level 1 pages to be created on
  * loginPage: the SharpSchool URL where you log in to the site
  * divName: the ID or class name of the <div> which contains the content on the old site
4. Make sure CMS Extension is running.
5. Run the program!