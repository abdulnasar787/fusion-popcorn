FUSION POPCORN — DJANGO WEBSITE (10 PAGES)
==========================================

ഈ project Windows + VS Code-ൽ run ചെയ്യാൻ:

1. ZIP extract ചെയ്യുക.
2. VS Code തുറക്കുക → File → Open Folder → fusion_popcorn_django folder.
3. Terminal → New Terminal.
4. താഴെയുള്ള commands ഓരോന്നായി run ചെയ്യുക:

   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   py -m pip install -r requirements.txt
   py manage.py makemigrations
   py manage.py migrate
   py manage.py runserver

5. Chrome-ൽ http://127.0.0.1:8000/ തുറക്കുക.

പ്രധാന pages:
Home        /
Shop        /shop/
Product     /product/classic/
Offers      /offers/
Cart        /cart/
Checkout    /checkout/
Payment     /payment/ (checkout form submit ചെയ്തശേഷം)
About       /about/
Gallery     /gallery/
Contact     /contact/

കുറിപ്പുകൾ:
- Product cards-ൽ emoji illustrations ആണ്. പിന്നീട് യഥാർത്ഥ product images ചേർക്കാം.
- Cart session ഉപയോഗിക്കുന്നു; checkout orders SQLite database-ൽ save ചെയ്യും.
- Payment page ഇപ്പോൾ PLACEHOLDER മാത്രമാണ്. ഇത് പണം സ്വീകരിക്കുന്നില്ല.
- Razorpay integration ചേർക്കുന്നതിന് മുമ്പ് Test Mode API keys, server-side order creation,
  signature verification, payment status/capture verification, duplicate callback handling,
  webhook verification എന്നിവ ശരിയായി implement/test ചെയ്യണം.
- Production-ൽ SECRET_KEY environment variable-ലേക്ക് മാറ്റുക, DEBUG=False,
  proper ALLOWED_HOSTS, HTTPS, database backups, privacy/food business requirements എന്നിവ configure ചെയ്യുക.
- Customer card details, UPI PIN, bank passwords ഒരിക്കലും സ്വന്തം form-ൽ ചോദിക്കരുത്.
