```json
"example_id": 797803103760793766,
"question_text": "who founded google",
"question_tokens": ["who", "founded", "google"],
"document_url": "http://www.wikipedia.org/Google",
"document_html": "<html><body><h1>Google Inc.</h1><p>Google was founded in 1998 By:<ul><li>Larry</li><li>Sergey</li></ul></p></body></html>",
"document_tokens":[
  { "token": "<h1>", "start_byte": 12, "end_byte": 16, "html_token": True },
  { "token": "Google", "start_byte": 16, "end_byte": 22, "html_token": False },
  { "token": "inc", "start_byte": 23, "end_byte": 26, "html_token": False },
  { "token": ".", "start_byte": 26, "end_byte": 27, "html_token": False },
  { "token": "</h1>", "start_byte": 27, "end_byte": 32, "html_token": True },
  { "token": "<p>", "start_byte": 32, "end_byte": 35, "html_token": True },
  { "token": "Google", "start_byte": 35, "end_byte": 41, "html_token": False },
  { "token": "was", "start_byte": 42, "end_byte": 45, "html_token": False },
  { "token": "founded", "start_byte": 46, "end_byte": 53, "html_token": False },
  { "Token": "in", "start_byte": 54, "end_byte": 56, "html_token": False },
  { "token": "1998", "start_byte": 57, "end_byte": 61, "html_token": False },
  { "token": "by", "start_byte": 62, "end_byte": 64, "html_token": False },
  { "token": ":", "start_byte": 64, "end_byte": 65, "html_token": False },
  { "token": "<ul>", "start_byte": 65, "end_byte": 69, "html_token": True },
  { "token": "<li>", "start_byte": 69, "end_byte": 73, "html_token": True },
  { "token": "Larry", "start_byte": 73, "end_byte": 78, "html_token": False },
  { "token": "</li>", "start_byte": 78, "end_byte": 83, "html_token": True },
  { "token": "<li>", "start_byte": 83, "end_byte": 87, "html_token": True },
  { "token": "Sergey", "start_byte": 87, "end_byte": 92, "html_token": False },
  { "token": "</li>", "start_byte": 92, "end_byte": 97, "html_token": True },
  { "token": "</ul>", "start_byte": 97, "end_byte": 102, "html_token": True },
  { "token": "</p>", "start_byte": 102, "end_byte": 106, "html_token": True }
],
"long_answer_candidates": [
  { "start_byte": 32, "end_byte": 106, "start_token": 5, "end_token": 22, "top_level": True },
  { "start_byte": 65, "end_byte": 102, "start_token": 13, "end_token": 21, "top_level": False },
  { "start_byte": 69, "end_byte": 83, "start_token": 14, "end_token": 17, "top_level": False },
  { "start_byte": 83, "end_byte": 92, "start_token": 17, "end_token": 20 , "top_level": False }
],
"annotations": [{
  "long_answer": { "start_byte": 32, "end_byte": 106, "start_token": 5, "end_token": 22, "candidate_index": 0 },
  "short_answers": [
    {"start_byte": 73, "end_byte": 78, "start_token": 15, "end_token": 16},
    {"start_byte": 87, "end_byte": 92, "start_token": 18, "end_token": 19}
  ],
  "yes_no_answer": "NONE"
}]
```
