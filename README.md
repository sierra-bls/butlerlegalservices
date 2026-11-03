# Butler Legal Services website

Static site for Netlify. Publish folder: `site/`. Pages: home, services, small claims, traffic tickets, minor criminal, provincial offences, limited scope,
Durham Region, five situation pages (speeding, stunt driving, careless driving, been sued, unpaid invoice), about, FAQ, contact (Netlify form), thank-you, privacy, terms, 404.

## Fill these in (all in build/build_site.py, CONFIG block at the top), then rebuild
python3 build/build_site.py site   (copy build/styles.css to site/ if you change styles)
- PHONE: leave None until you have a number. When set, phone links, header number and the mobile Call button appear everywhere.
- ADDRESS, GA_ID (Google Analytics), INSTAGRAM, TIKTOK: None means left out.
- PRICES, FREE_CALL_LENGTH, STRATEGY_LENGTH, BOOKING_URL: fill in once decided; prices show "Quoted in writing" until then. Strategy consultation price is the main one to set.
- LICENSEE: currently "Sierra Walker" (name on the LSO licence). Confirm with the LSO what name to advertise under.

## Before launch
1. New GitHub repo and new Netlify site; point butlerlegalservices.ca DNS (GoDaddy) at it.
2. Netlify > Forms: turn on email notification for the "consultation" form to sierra@ or hello@.
3. Add a photo and your court experience to the About page if you want them.
4. Replace logo.png and favicons if you commission a real logo (same file names).
5. Have the LSO Practice Management Helpline review the copy, fee wording and the name "Butler Legal Services".
6. Google Search Console + Google Business Profile, then submit sitemap.xml.

Removed from the Notable Notary template: all notary, apostille and translation pages, order pages, order tracking,
Netlify functions, GHL IDs, chat widget, review claims and old Google Analytics ID.

Photo: site/sierra.jpg is the Notable Notary chat avatar used as a stand-in. Replace it with a proper headshot (same file name, square).
Reviews: the homepage and About page show Notable Notary's 5.0 / 200+ Google reviews, labelled as notary reviews. Have the LSO helpline confirm this is acceptable.

SEO: submit sitemap.xml in Search Console, claim the Google Business Profile, list on the LSO directory, link to this site from notablenotary.ca, and ask clients for Google reviews. llms.txt helps AI tools understand the site.
The old Fees page was folded into the Services and Contact pages; /fees redirects to /contact.
