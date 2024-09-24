import unittest
import jamorasep


class TestJpmorasep(unittest.TestCase):

    def test_katakana(self):
        """
        Test: Convert a list of Katakana into a list of morae
        If the output format is None, then return the output in the form of list of morae
        """
        self.assertEqual(jamorasep.parse('アイウエオ'), ['ア', 'イ', 'ウ', 'エ', 'オ'])
        self.assertEqual(jamorasep.parse('カキクケコ'), ['カ', 'キ', 'ク', 'ケ', 'コ'])
        self.assertEqual(jamorasep.parse('サシスセソ'), ['サ', 'シ', 'ス', 'セ', 'ソ'])
        self.assertEqual(jamorasep.parse('タチツテト'), ['タ', 'チ', 'ツ', 'テ', 'ト'])
        self.assertEqual(jamorasep.parse('ナニヌネノ'), ['ナ', 'ニ', 'ヌ', 'ネ', 'ノ'])
        self.assertEqual(jamorasep.parse('ハヒフヘホ'), ['ハ', 'ヒ', 'フ', 'ヘ', 'ホ'])
        self.assertEqual(jamorasep.parse('マミムメモ'), ['マ', 'ミ', 'ム', 'メ', 'モ'])
        self.assertEqual(jamorasep.parse('ヤユヨ'), ['ヤ', 'ユ', 'ヨ'])
        self.assertEqual(jamorasep.parse('ラリルレロ'), ['ラ', 'リ', 'ル', 'レ', 'ロ'])
        self.assertEqual(jamorasep.parse('ワヲン'), ['ワ', 'ヲ', 'ン'])
        self.assertEqual(jamorasep.parse('ガギグゲゴ'), ['ガ', 'ギ', 'グ', 'ゲ', 'ゴ'])
        self.assertEqual(jamorasep.parse('ザジズゼゾ'), ['ザ', 'ジ', 'ズ', 'ゼ', 'ゾ'])
        self.assertEqual(jamorasep.parse('ダヂヅデド'), ['ダ', 'ヂ', 'ヅ', 'デ', 'ド'])
        self.assertEqual(jamorasep.parse('バビブベボ'), ['バ', 'ビ', 'ブ', 'ベ', 'ボ'])
        self.assertEqual(jamorasep.parse('パピプペポ'), ['パ', 'ピ', 'プ', 'ペ', 'ポ'])
        self.assertEqual(jamorasep.parse('ヴァヴィヴヴェヴォ'), ['ヴァ', 'ヴィ', 'ヴ', 'ヴェ', 'ヴォ'])
        self.assertEqual(jamorasep.parse('キャキュキェキョ'), ['キャ', 'キュ', 'キェ', 'キョ'])
        self.assertEqual(jamorasep.parse('シャシュシェショ'), ['シャ', 'シュ', 'シェ', 'ショ'])
        self.assertEqual(jamorasep.parse('チャチュチェチョ'), ['チャ', 'チュ', 'チェ', 'チョ'])
        self.assertEqual(jamorasep.parse('ツァツィツェツォ'), ['ツァ', 'ツィ', 'ツェ', 'ツォ'])
        self.assertEqual(jamorasep.parse('ニャニュニェニョ'), ['ニャ', 'ニュ', 'ニェ', 'ニョ'])
        self.assertEqual(jamorasep.parse('ヒャヒュヒェヒョ'), ['ヒャ', 'ヒュ', 'ヒェ', 'ヒョ'])
        self.assertEqual(jamorasep.parse('ミャミュミェミョ'), ['ミャ', 'ミュ', 'ミェ', 'ミョ'])
        self.assertEqual(jamorasep.parse('リャリュリェリョ'), ['リャ', 'リュ', 'リェ', 'リョ'])
        self.assertEqual(jamorasep.parse('ギャギュギェギョ'), ['ギャ', 'ギュ', 'ギェ', 'ギョ'])
        self.assertEqual(jamorasep.parse('ジャジュジェジョ'), ['ジャ', 'ジュ', 'ジェ', 'ジョ'])
        self.assertEqual(jamorasep.parse('ビャビュビェビョ'), ['ビャ', 'ビュ', 'ビェ', 'ビョ'])
        self.assertEqual(jamorasep.parse('ピャピュピェピョ'), ['ピャ', 'ピュ', 'ピェ', 'ピョ'])
        self.assertEqual(jamorasep.parse('ファフィフェフォ'), ['ファ', 'フィ', 'フェ', 'フォ'])
        self.assertEqual(jamorasep.parse('ウィウェウォ'), ['ウィ', 'ウェ', 'ウォ'])
        self.assertEqual(jamorasep.parse('クァクィクェクォ'), ['クァ', 'クィ', 'クェ', 'クォ'])
        self.assertEqual(jamorasep.parse('グァグィグェグォ'), ['グァ', 'グィ', 'グェ', 'グォ'])
        self.assertEqual(jamorasep.parse('ティディ'), ['ティ', 'ディ'])
        self.assertEqual(jamorasep.parse('トゥドゥ'), ['トゥ', 'ドゥ'])
        self.assertEqual(jamorasep.parse('テュデュ'), ['テュ', 'デュ'])
        self.assertEqual(jamorasep.parse('テェデェ'), ['テェ', 'デェ'])
        self.assertEqual(jamorasep.parse('テョデョ'), ['テョ', 'デョ'])
        self.assertEqual(jamorasep.parse('スィズィ'), ['スィ', 'ズィ'])

    def test_hiragana(self):
        """
        Test: Convert a list of hiragana into a list of morae
        If the output format is None, then return the output in the form of list of morae
        """
        self.assertEqual(jamorasep.parse('あいうえお'), ['あ', 'い', 'う', 'え', 'お'])
        self.assertEqual(jamorasep.parse('かきくけこ'), ['か', 'き', 'く', 'け', 'こ'])
        self.assertEqual(jamorasep.parse('さしすせそ'), ['さ', 'し', 'す', 'せ', 'そ'])
        self.assertEqual(jamorasep.parse('たちつてと'), ['た', 'ち', 'つ', 'て', 'と'])
        self.assertEqual(jamorasep.parse('なにぬねの'), ['な', 'に', 'ぬ', 'ね', 'の'])
        self.assertEqual(jamorasep.parse('はひふへほ'), ['は', 'ひ', 'ふ', 'へ', 'ほ'])
        self.assertEqual(jamorasep.parse('まみむめも'), ['ま', 'み', 'む', 'め', 'も'])
        self.assertEqual(jamorasep.parse('やゆよ'), ['や', 'ゆ', 'よ'])
        self.assertEqual(jamorasep.parse('らりるれろ'), ['ら', 'り', 'る', 'れ', 'ろ'])
        self.assertEqual(jamorasep.parse('わをん'), ['わ', 'を', 'ん'])
        self.assertEqual(jamorasep.parse('がぎぐげご'), ['が', 'ぎ', 'ぐ', 'げ', 'ご'])
        self.assertEqual(jamorasep.parse('ざじずぜぞ'), ['ざ', 'じ', 'ず', 'ぜ', 'ぞ'])
        self.assertEqual(jamorasep.parse('だぢづでど'), ['だ', 'ぢ', 'づ', 'で', 'ど'])
        self.assertEqual(jamorasep.parse('ばびぶべぼ'), ['ば', 'び', 'ぶ', 'べ', 'ぼ'])
        self.assertEqual(jamorasep.parse('ぱぴぷぺぽ'), ['ぱ', 'ぴ', 'ぷ', 'ぺ', 'ぽ'])
        self.assertEqual(jamorasep.parse('ゔぁゔぃゔゔぇゔぉ'), ['ゔぁ', 'ゔぃ', 'ゔ', 'ゔぇ', 'ゔぉ'])
        self.assertEqual(jamorasep.parse('きゃきゅきぇきょ'), ['きゃ', 'きゅ', 'きぇ', 'きょ'])
        self.assertEqual(jamorasep.parse('しゃしゅしぇしょ'), ['しゃ', 'しゅ', 'しぇ', 'しょ'])
        self.assertEqual(jamorasep.parse('ちゃちゅちぇちょ'), ['ちゃ', 'ちゅ', 'ちぇ', 'ちょ'])
        self.assertEqual(jamorasep.parse('つぁつぃつぇつぉ'), ['つぁ', 'つぃ', 'つぇ', 'つぉ'])
        self.assertEqual(jamorasep.parse('にゃにゅにぇにょ'), ['にゃ', 'にゅ', 'にぇ', 'にょ'])
        self.assertEqual(jamorasep.parse('ひゃひゅひぇひょ'), ['ひゃ', 'ひゅ', 'ひぇ', 'ひょ'])
        self.assertEqual(jamorasep.parse('みゃみゅみぇみょ'), ['みゃ', 'みゅ', 'みぇ', 'みょ'])
        self.assertEqual(jamorasep.parse('りゃりゅりぇりょ'), ['りゃ', 'りゅ', 'りぇ', 'りょ'])
        self.assertEqual(jamorasep.parse('ぎゃぎゅぎぇぎょ'), ['ぎゃ', 'ぎゅ', 'ぎぇ', 'ぎょ'])
        self.assertEqual(jamorasep.parse('じゃじゅじぇじょ'), ['じゃ', 'じゅ', 'じぇ', 'じょ'])
        self.assertEqual(jamorasep.parse('びゃびゅびぇびょ'), ['びゃ', 'びゅ', 'びぇ', 'びょ'])
        self.assertEqual(jamorasep.parse('ぴゃぴゅぴぇぴょ'), ['ぴゃ', 'ぴゅ', 'ぴぇ', 'ぴょ'])
        self.assertEqual(jamorasep.parse('ふぁふぃふぇふぉ'), ['ふぁ', 'ふぃ', 'ふぇ', 'ふぉ'])
        self.assertEqual(jamorasep.parse('うぃうぇうぉ'), ['うぃ', 'うぇ', 'うぉ'])
        self.assertEqual(jamorasep.parse('くぁくぃくぇくぉ'), ['くぁ', 'くぃ', 'くぇ', 'くぉ'])
        self.assertEqual(jamorasep.parse('ぐぁぐぃぐぇぐぉ'), ['ぐぁ', 'ぐぃ', 'ぐぇ', 'ぐぉ'])
        self.assertEqual(jamorasep.parse('てぃでぃ'), ['てぃ', 'でぃ'])
        self.assertEqual(jamorasep.parse('とぅどぅ'), ['とぅ', 'どぅ'])
        self.assertEqual(jamorasep.parse('てゅでゅ'), ['てゅ', 'でゅ'])
        self.assertEqual(jamorasep.parse('てぇでぇ'), ['てぇ', 'でぇ'])
        self.assertEqual(jamorasep.parse('てょでょ'), ['てょ', 'でょ'])
        self.assertEqual(jamorasep.parse('ふぃふぇ'), ['ふぃ', 'ふぇ'])
        self.assertEqual(jamorasep.parse('ふゃふゅふぉ'), ['ふゃ', 'ふゅ', 'ふぉ'])

    def test_mixed(self):
        """
        Test: Convert a list of mixed characters into a list of morae
        If the output format is "None", then return the output in the form of list of morae
        """
        self.assertEqual(jamorasep.parse('キゃきュきェキょ'), ['キゃ', 'きュ', 'きェ', 'キょ'])

    def test_romanize_kunrei(self):
        """
        Test: Convert a string of Katakana into a list of morae.
        The output of the input string is determined by the desired format. 
        First, check if the input string is present in the kana map headers and convert it to Katakana. 
        Next, verify if the value is Katakana and retrieve the corresponding output from the kana map. 
        Then, apply special mora modifications unless the output format is "simple-ipa," and check if the "phoneme" is true, if yes, then join the modified morae into a string and convert it to a list. 
        Finally, return the output as a list of morae; otherwise, print the list of morae.
        """
        self.assertEqual(jamorasep.parse('キゃきュきェキょ', output_format="kunrei"), ['kya', 'kyu', 'kye', 'kyo'])
        self.assertEqual(jamorasep.parse('ワヲン', output_format="simple-ipa"), ['wa', 'o', 'N'])
        self.assertEqual(jamorasep.parse('ワヲン', output_format="kunrei"), ['wa', 'o', 'n'])

    def test_Q(self):
        """
        Test: Convert a string of Katakana into a list of morae.
        The output of the input string is determined by the desired format. 
        First, check if the input string is present in the kana map headers and convert it to Katakana. 
        Next, verify if the value is Katakana and retrieve the corresponding output from the kana map. 
        Then, apply special mora modifications unless the output format is "simple-ipa," and check if the "phoneme" is true, if yes, then join the modified morae into a string and convert it to a list. 
        Finally, return the output as a list of morae; otherwise, print the list of morae.
        """
        self.assertEqual(jamorasep.parse('カッキックッケッコッ'), ['カ', 'ッ', 'キ', 'ッ', 'ク', 'ッ', 'ケ', 'ッ', 'コ', 'ッ'])
        self.assertEqual(jamorasep.parse('アッイッウッエッオッ'), ['ア', 'ッ', 'イ', 'ッ', 'ウ', 'ッ', 'エ', 'ッ', 'オ', 'ッ'])
        self.assertEqual(jamorasep.parse('カッキックッケッコッ',output_format="kunrei"), ['ka', 'k', 'ki', 'k', 'ku', 'k', 'ke', 'k', 'ko', ' '])
        self.assertEqual(jamorasep.parse('アッイッウッエッオッ',output_format="kunrei"), ['a', ' ', 'i', ' ', 'u', ' ', 'e', ' ', 'o', ' '])
        self.assertEqual(jamorasep.parse('カッッッッキッッッックッッッッケッッッッコッッッッ',output_format="kunrei"),
                        ['ka', 'k', 'k', 'k', 'k',
                         'ki', 'k', 'k', 'k', 'k',
                         'ku', 'k', 'k', 'k', 'k',
                         'ke', 'k', 'k', 'k', 'k',
                         'ko', ' ', ' ', ' ', ' '])
        self.assertEqual(jamorasep.parse('シャッシュッショッ',output_format="kunrei"),
                         ['sya', 's', 'syu', 's', 'syo', ' '])
        self.assertEqual(jamorasep.parse('シャッシュッショッ',output_format="kunrei", phoneme=True),
                         ['s', 'y', 'a', 's', 's', 'y', 'u', 's', 's', 'y', 'o', ' '])
        self.assertEqual(jamorasep.parse('しょっぱい'),
                         ['しょ', 'っ', 'ぱ', 'い'])
        self.assertEqual(jamorasep.parse('ッッッッッ'), ['ッ'] * 5),
        self.assertEqual(jamorasep.parse('ッッッッッ', output_format="simple-ipa"), ['Q'] * 5),
        self.assertEqual(jamorasep.parse('ッッッッッ', output_format="kunrei"), [' '] * 5),
        self.assertEqual(jamorasep.parse('ッッッッッ。', output_format="kunrei"), [' '] * 5 + ['。']),
        self.assertEqual(jamorasep.parse('ッ。ッ。ッ。ッ。ッ。', output_format="kunrei"), [' ', '。'] * 5),
        self.assertEqual(jamorasep.parse('アッカッサッタッチッナッハッマッヤッラッワッガッザッジャッダッバッパッヴァッア', output_format="hepburn"),
                         ['a', 'k', 'ka', 's', 'sa', 't', 'ta', 'c', 'chi',
                          'n', 'na', 'h', 'ha', 'm', 'ma', 'y', 'ya', 'r', 'ra',
                          'w', 'wa', 'g', 'ga', 'z', 'za', 'j', 'ja', 'd', 'da',
                          'b', 'ba', 'p', 'pa', 'v', 'va', ' ', 'a']),
        self.assertEqual(jamorasep.parse('ッカ', output_format="kunrei"), ['k', 'ka']),
        self.assertEqual(jamorasep.parse('ッア', output_format="kunrei"), [' ', 'a']),

    def test_successive_small(self):
        """
        Test: Convert a string of katakana into a list of morae
        If the ouput fromat is "None", the output is a list of morae.
        """
        self.assertEqual(jamorasep.parse('アイウキャカァィゥエ'),
                         ['ア', 'イ', 'ウ', 'キャ', 'カ', 'ア', 'イ', 'ウ', 'エ'])
        self.assertEqual(jamorasep.parse('ァァァィィィィゥゥゥゥゥェェ'),
                         ['ア'] * 3 + ['イ'] * 4 + ['ウ'] * 5 + ['エ'] * 2)
        self.assertEqual(jamorasep.parse('ァアィイゥウェエォオ'),
                         ['ア'] * 2 + ['イ'] * 2 + ['ウ', 'ウェ', 'エ'] + ['オ'] * 2)

    def test_specific_words(self):
        """
        Test: Convert a string of katakana into a list of morae
        If the ouput fromat is "None", the output is a list of morae.
        """
        self.assertEqual(jamorasep.parse('ジョスカン・デ・プレ'),
                         ['ジョ', 'ス', 'カ', 'ン', '・', 'デ', '・', 'プ', 'レ'])
        self.assertEqual(jamorasep.parse('ヴォルフガング・アマデウス・モーツァルト'),
                         ['ヴォ', 'ル', 'フ', 'ガ', 'ン', 'グ', '・', 'ア', 'マ', 'デ', 'ウ', 'ス', '・', 'モ', 'ー', 'ツァ', 'ル', 'ト'])
        self.assertEqual(jamorasep.parse('ルートヴィヒ・ヴァン・ベートーヴェン'),
                         ['ル', 'ー', 'ト', 'ヴィ', 'ヒ', '・', 'ヴァ', 'ン', '・', 'ベ', 'ー', 'ト', 'ー', 'ヴェ', 'ン'])
        self.assertEqual(jamorasep.parse('シェーンベルク'),
                         ['シェ', 'ー', 'ン', 'ベ', 'ル', 'ク']),
        self.assertEqual(jamorasep.parse('エイトクィーン'),
                         ['エ', 'イ', 'ト', 'クィ', 'ー', 'ン'])
        self.assertEqual(jamorasep.parse('ディープラーニング'), [
            'ディ', 'ー', 'プ', 'ラ', 'ー', 'ニ', 'ン', 'グ'])
    
    def test_output_format_hiragana(self):
        """
        Test: Convert a list of Katakana morae to Hiragana
        If the output format is "hiragana", checks if the mora is in kanamap keys and converts katakana to hiragana.
        """
        self.assertEqual(jamorasep.parse('アイウエオ', output_format="hiragana"), ['あ', 'い', 'う', 'え', 'お'])
        self.assertEqual(jamorasep.parse('カキクケコ', output_format="hiragana"), ['か', 'き', 'く', 'け', 'こ'])
        self.assertEqual(jamorasep.parse('サシスセソ', output_format="hiragana"), ['さ', 'し', 'す', 'せ', 'そ'])
        self.assertEqual(jamorasep.parse('タチツテト', output_format="hiragana"), ['た', 'ち', 'つ', 'て', 'と'])
        self.assertEqual(jamorasep.parse('ナニヌネノ', output_format="hiragana"), ['な', 'に', 'ぬ', 'ね', 'の'])
        self.assertEqual(jamorasep.parse('ハヒフヘホ', output_format="hiragana"), ['は', 'ひ', 'ふ', 'へ', 'ほ'])
        self.assertEqual(jamorasep.parse('マミムメモ', output_format="hiragana"), ['ま', 'み', 'む', 'め', 'も'])
        self.assertEqual(jamorasep.parse('ヤユヨ', output_format="hiragana"), ['や', 'ゆ', 'よ'])
        self.assertEqual(jamorasep.parse('ラリルレロ', output_format="hiragana"), ['ら', 'り', 'る', 'れ', 'ろ'])
        self.assertEqual(jamorasep.parse('ワヲン', output_format="hiragana"), ['わ', 'を', 'ん'])

    def test_output_format_katakana(self):
        """
        Test: Convert a list of Hiragana morae to Katakana
        If the output format is "katakana", checks if the mora is in kanamap keys and converts hiragana to katakana.
        """
        self.assertEqual(jamorasep.parse('あいうえお', output_format="katakana"), ['あ', 'い', 'う', 'え', 'お'])
        self.assertEqual(jamorasep.parse('かきくけこ', output_format="katakana"), ['か', 'き', 'く', 'け', 'こ'])
        self.assertEqual(jamorasep.parse('さしすせそ', output_format="katakana"), ['さ', 'し', 'す', 'せ', 'そ'])
        self.assertEqual(jamorasep.parse('たちつてと', output_format="katakana"), ['た', 'ち', 'つ', 'て', 'と'])
        self.assertEqual(jamorasep.parse('なにぬねの', output_format="katakana"), ['な', 'に', 'ぬ', 'ね', 'の'])
        self.assertEqual(jamorasep.parse('はひふへほ', output_format="katakana"), ['は', 'ひ', 'ふ', 'へ', 'ほ'])
        self.assertEqual(jamorasep.parse('まみむめも', output_format="katakana"), ['ま', 'み', 'む', 'め', 'も'])
        self.assertEqual(jamorasep.parse('やゆよ', output_format="katakana"), ['や', 'ゆ', 'よ'])
        self.assertEqual(jamorasep.parse('らりるれろ', output_format="katakana"), ['ら', 'り', 'る', 'れ', 'ろ'])
        self.assertEqual(jamorasep.parse('わをん', output_format="katakana"), ['わ', 'を', 'ん'])


if __name__ == '__main__':
    unittest.main()