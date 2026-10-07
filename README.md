# dromeasnews.com

The public website of Dromeas News: home page, privacy policy and account-deletion page, hosted free by GitHub Pages.

- Page texts are in `src/*.md`; `python3 build.py` turns them into the HTML pages (needs pandoc). Claude edits and
  rebuilds them; the founder's steps are in the Founder Guide (Flyer repository, `docs/Dromeas_Founder_Guide.docx`).
- The privacy policy's "last updated" date is `UPDATED` in `build.py`.
- `CNAME` holds the domain; DNS is at GoDaddy (4 A records for GitHub Pages + `www` CNAME).
