import csv,hashlib,json,pathlib,re,subprocess,unittest,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
class TestProducedData(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads((ROOT/'processing/reports/summary.json').read_text('utf-8'))
 def test_original_files_immutable(self):
  for name,expected in self.report['source_sha256'].items():
   path=ROOT/'processing/raw'/name
   self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected)
  self.assertTrue(self.report['integrity']['original_files_unchanged'])
 def test_record_counts_and_identifiers_preserved(self):
  a=ROOT/'processing/raw/records.original.zip'
  b=ROOT/'data/records.zip'
  with zipfile.ZipFile(a) as before,zipfile.ZipFile(b) as after:
   self.assertEqual(before.namelist(),after.namelist())
   total=0
   for name in before.namelist():
    if not name.endswith('.bib'):continue
    aa=before.read(name).decode('utf-8')
    bb=after.read(name).decode('utf-8')
    ids=lambda s:re.findall(r'^\s*@\w+\s*\{\s*([^,]+),',s,re.M)
    self.assertEqual(ids(aa),ids(bb),f'changed IDs: {name}')
    total+=len(ids(aa))
   self.assertEqual(total,150656)
 def test_catalog_size_and_source_consistency(self):
  catalog=json.loads((ROOT/'data/catalog.json').read_text('utf-8'))
  sources=json.loads((ROOT/'data/sources.json').read_text('utf-8'))
  self.assertEqual(len(catalog),4003)
  self.assertEqual(len(sources),203)
  self.assertEqual(sum(x['records'] for x in sources),150656)
  self.assertEqual(len([c for c in catalog if not c.get('url')]),1)
 def test_manual_review_has_stable_ids(self):
  with (ROOT/'processing/reports/manual_review.csv').open(encoding='utf-8-sig',newline='') as f:
   cases=list(csv.DictReader(f))
  self.assertGreater(len(cases),0)
  self.assertTrue(all(len(case['case_id'])==16 and case['status'] in {'do_sprawdzenia','rozpatrzono'} for case in cases))
  codes={case['code'] for case in cases}
  self.assertIn('suspicious_year',codes)
  self.assertIn('ambiguous_and',codes)
  self.assertIn('invalid_catalog_url',codes)
 def test_automated_search_module(self):
  js=ROOT/'processing/tests/test_search.cjs'
  status=subprocess.run(['node',str(js)],capture_output=True,text=True,cwd=ROOT)
  self.assertEqual(status.returncode,0,status.stdout+'\n'+status.stderr)
