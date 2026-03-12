const fs = require('fs');
const { google } = require('googleapis');

const FILE_ID = '1E_85gSF_38dpfrLNj67KOrt-fFru3Q4k';
const OUT = 'kis-trading-bot-package.tar.gz';

async function main() {
  const creds = JSON.parse(fs.readFileSync('client_secret.json', 'utf8')).installed;
  const token = JSON.parse(fs.readFileSync('token.json', 'utf8'));

  const auth = new google.auth.OAuth2(creds.client_id, creds.client_secret, creds.redirect_uris[0]);
  auth.setCredentials(token);

  const drive = google.drive({ version: 'v3', auth });

  const dest = fs.createWriteStream(OUT);
  const res = await drive.files.get({ fileId: FILE_ID, alt: 'media' }, { responseType: 'stream' });

  await new Promise((resolve, reject) => {
    res.data.on('end', resolve).on('error', reject).pipe(dest);
  });

  console.log('Downloaded:', OUT);
}

main().catch((e) => {
  console.error(e?.response?.data || e.message || e);
  process.exit(1);
});
