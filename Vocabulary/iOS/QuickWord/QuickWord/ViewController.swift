//
//  ViewController.swift
//  QuickWord
//
//  Created by Abdulrahman Alattas on 2019-01-11.
//  Copyright © 2019 Abdulrahman Alattas. All rights reserved.
//

import UIKit
import Foundation

class ViewController: UIViewController {

    @IBOutlet weak var btnSearch: UIButton!
    @IBOutlet weak var txtWord: UITextField!
    @IBOutlet weak var txtInfo: UITextView!
    @IBOutlet weak var indWait: UIActivityIndicatorView!
    
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }
    
    @IBAction func btnSearchClick(_ sender: Any) {
        printWordInfo(word:txtWord.text!)
    }
    
    func printWordInfo(word:String){
        let word_info : WordInfo = getWordInfo(word: word);
        var word_info_text : String = "";
        for def in word_info.definition{
            word_info_text += def + "\n";
        }
        txtInfo.text = word_info_text;
    }
    
    func getWordInfo(word:String) -> WordInfo{
        let word_info: WordInfo = WordInfo()
        
        indWait.startAnimating();
        word_info.definition = getWordDefs(word:word)
        
        indWait.stopAnimating();
        
        return word_info;
    }
    
    func getWordDefs(word:String) -> [String] {
        var result: [String] = []
        let urlString = "https://api.wordnik.com/v4/word.json/" + word + "/definitions?limit=200&includeRelated=false&useCanonical=false&includeTags=false&api_key=81f2dc26478d5bb9700080628d306bca63bc5847e039516aa"
        let url = URL(string: urlString)
        URLSession.shared.dataTask(with: url!) { (data, response, error) in
            if error != nil {
                print(error!.localizedDescription)
            }

            guard let data = data else { return }
            print(data);
            //Implement JSON decoding and parsing
            struct WordDef: Decodable { var text: String; }
            var word_def_list : [WordDef] = [];
            do {
                //Decode retrived data with JSONDecoder and assing type of Article object
                word_def_list = try JSONDecoder().decode([WordDef].self, from: data)
                print(word_def_list)
            } catch let jsonError {
                print(jsonError)
            }
            
            for word_def in word_def_list{
                result.append(word_def.text)
            }
            
            }.resume()
        
        return result;
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }


}

class WordInfo{
    var definition: [String] = [];
    var examples: [String] = [];
    var synonyms: [String] = [];
}

