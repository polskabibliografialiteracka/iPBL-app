import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'processing'))
from normalization import strip_safe_escapes,split_authors,normalize_urls,safe_url,author_labels,normalize_type
class TestNormalization(unittest.TestCase):
 def test_latex_escapes_and_unknown_commands(self):
  self.assertEqual(strip_safe_escapes(r'Sex, drugs \& rock\_n\#roll'),'Sex, drugs & rock_n#roll')
  self.assertEqual(strip_safe_escapes(r'\textit{Słowo} \\&'),r'\textit{Słowo} \\&')
 def test_bibtex_author_split(self):
  val,split,manual=split_authors('Honet, Roman and Sala, Zuzanna')
  self.assertEqual(val,'Honet, Roman | Sala, Zuzanna')
  self.assertTrue(split);self.assertFalse(manual)
  val,split,manual=split_authors('Dobrego ankietera and po gaszeniu na ciele')
  self.assertFalse(split);self.assertTrue(manual)
  val,split,manual=split_authors('(VIAF:https://viaf.org/viaf/123/), Sylwia Pikula and Kowalska, Anna')
  self.assertTrue(split);self.assertFalse(manual)
  self.assertEqual(author_labels(val),['Sylwia Pikula','Kowalska, Anna'])
 def test_url_cleanup_and_wayback(self):
  src=(r'http://www.afiszteatralny.pl/daje-flow\_15.html, '
       r'https://web.archive.org/web/20240701/http://www.afiszteatralny.pl/daje-flow\_15.html')
  val,issues=normalize_urls(src)
  self.assertIn('daje-flow_15.html',val)
  self.assertNotIn('\\',val)
  self.assertEqual(issues,[])
 def test_invalid_urls(self):
  self.assertEqual(safe_url('Found in Translation - Instytut Książki',True)[0],'')
  self.assertEqual(safe_url(r'\#ERROR!')[0],'')
  self.assertEqual(safe_url('javascript:alert(1)',True)[0],'')
  self.assertEqual(safe_url('literackie-skarby.blogspot.com',True),
                   ('https://literackie-skarby.blogspot.com','added_https'))
 def test_orthographic_only(self):
  self.assertEqual(normalize_type('kanał księgarni (Youtube)'),'kanał księgarni (YouTube)')
