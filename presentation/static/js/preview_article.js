function htmlspecialchars_decode (string, quoteStyle) {
  let optTemp = 0
  let i = 0
  let noquotes = false
  if (typeof quoteStyle === 'undefined') {
    quoteStyle = 2
  }
  let width = $("#content").width() - 35;
  string = string.toString()
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&#34;/g, '"')
    .replace("img", "img style=\"max-width:" + width + "px;\"")
  const OPTS = {
    ENT_NOQUOTES: 0,
    ENT_HTML_QUOTE_SINGLE: 1,
    ENT_HTML_QUOTE_DOUBLE: 2,
    ENT_COMPAT: 2,
    ENT_QUOTES: 3,
    ENT_IGNORE: 4
  }
  if (quoteStyle === 0) {
    noquotes = true
  }
  if (typeof quoteStyle !== 'number') {
    quoteStyle = [].concat(quoteStyle)
    for (i = 0; i < quoteStyle.length; i++) {
      if (OPTS[quoteStyle[i]] === 0) {
        noquotes = true
      } else if (OPTS[quoteStyle[i]]) {
        optTemp = optTemp | OPTS[quoteStyle[i]]
      }
    }
    quoteStyle = optTemp
  }
  if (quoteStyle & OPTS.ENT_HTML_QUOTE_SINGLE) {
    string = string.replace(/&#0*39;/g, "'")
  }
  if (!noquotes) {
    string = string.replace(/&quot;/g, '"')
  }
  string = string.replace(/&amp;/g, '&')
  return string
}
