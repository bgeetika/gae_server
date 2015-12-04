# -*- coding: utf-8 -*-


import webapp2
import urllib2
import urllib

import json
import base64

class  MainPageJquery(webapp2.RequestHandler):
  def get(self):
    self.response.out.write(
		    """
		    <html>
                    <head>
		    <H1 align ="center">
		    <u align="center">
		    NEURAL NET CAPTCHA CRACKER
		    </u>
		    </H1>
		    <h3 align="center">
		    Project by: Geetika Garg
                    </h3>
		    <h3 align="center">
		    Project Advisor: Dr. Chris Pollett
		    <br><br>
                    </h3>
                    <div id="footer">
		    <ul>
				<p style="position: fixed; bottom: 0; width:100%; text-align: center">
				<a href="https://github.com/bgeetika/Captcha-Decoder">Project Github Link
				</a>
				</p>
	            </ul></div>
		    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
                    </head>
                    <body>

                    <form id = "generate" action ="/generate" method="get">
		    <input type ="submit" id = "sub" value="Generate and Decode any CAPTCHA"></input>
                    
		    </form>
                    <img id="res_image"/> 
                    <div id = "result_image"></div>

                    <script>
                    // Return decoded captcha with image
                    $( "#generate" ).submit(function( event ) {
                       console.log("generate");                    
                      // Stop form from submitting normally
                      event.preventDefault();
                      // Get some values from elements on the page:
                      url = $( this ).attr( "action" );
                        // Send the data using post
                        var posting = $.get(url);
                        // Put the results in a div
                        posting.done(function( data ) {
                          console.log(data);
                          var content = data["file_content"];
                          console.log(typeof(content));
                          var res = $( data ).find( "#answer" );
                          document.getElementById("res_image").src  = 'data:image/jpeg;base64,' + content;
                          $( "#result_image" ).empty().append("The CAPTCHA decodes to : " + data['answer'] );
                          $('#submit').hide();
                          $ ('#src').hide();
                          $('#model').hide();
                          var paragraph =  $('#instruct');
                          paragraph.hide();                      
                      });
                    });
                    </script>

                
		    
		    <form id="searchForm" enctype="multipart/form-data"  action="/submit_photo" method="post">
		    <p id="instruct" > Please upload an image-based CAPTCHA
		    </p>
		    <input id="src" type="file" name="datafile" size="500">
		    <img id="target"/> 
                    </p>
		    <p>
		    <select id = "model" name="model">
		      <option value="VariableLength">VariableLength</option>
		        <option value="Website">Website</option>
		        <option value="VariableFixed">VariableFixed</option>
		    </select>
		    </p>
		    <input type="submit" value="Send" id='submit' class='clickMe'>
                    </form>
                    <div id="result">
		     </div>

                    

                    <script>
                      function showImage(src,target) {
                        var fr=new FileReader();
                        // when image is loaded, set the src of the image where you want to display it
                        fr.onload = function(e) { target.src = this.result; };
                        src.addEventListener("change",function() {
                          // fill fr with image data    
                          fr.readAsDataURL(src.files[0]);
                        });
                      }
                      
                      var src = document.getElementById("src");
                      var target = document.getElementById("target");
                      showImage(src,target);                    
		      console.log("hidingbutton");
		      $(function(){
		              $('#submit').click(function() {
			                  $(this).hide();
					 $ ('#src').hide();
					 $('#model').hide();
					 $('#generate').hide();
					 var paragraph =  $('#instruct');
					 paragraph.hide();

					          });
						      });
		    </script>


                    <script>
                    // Attach a submit handler to the form
                    $( "#searchForm" ).submit(function( event ) {
                       console.log("submithandler");                    
                      // Stop form from submitting normally
                      event.preventDefault();
                      var model_name = $("#model").val();
                      // Get some values from elements on the page:
                      var $form = $( this ),
                        filepath = document.getElementById("src").files[0],
                        url = $form.attr( "action" );
                     
                      var fr = new FileReader();
                      fr.onload = function(e) {
                        var file_content = btoa(e.target.result);
                        
                        // Send the data using post
                        console.log('length of binary file: ' + e.target.result.length);
                        console.log('length of file: ' + file_content.length);
                        var posting = $.post( url, { datafile: file_content ,
			                             model: model_name} );
                     
                        // Put the results in a div
                        posting.done(function( data ) {
                          console.log(data);
                          //var content = $( data ).find( "#content" );
			  $( "#result" ).empty().append("The CAPTCHA decodes to : " + data['content'] );
                        });
                      }
                      console.log(filepath);
                      fr.readAsBinaryString(filepath);
                    });
                    </script>
                    </body>
                    </html>"""
		    )


class HandlePhoto(webapp2.RequestHandler):
     def post(self):
             print "here"
	     file_content = self.request.get('datafile')
	     model_name = self.request.get('model')
	     print model_name
	     print 'file_content', len(file_content), type(file_content), file_content[:10]
	     values = {'file_content' : file_content,
			     'model_name': model_name}
	     headers = {'content-type': 'application/json'}
	     url = "http://104.196.6.225:8080/"
	     #url = "http://104.154.65.114:8080/"
	     req = urllib2.Request(url=url)
	     method = "POST"
	     req.get_method = lambda: method
	     req.add_header('Content-Type', 'application/json')
	     print type(json.dumps(values))
	     f = urllib2.urlopen(req, data = json.dumps(values))
	     the_page = f.read()
             self.response.headers['Content-Type'] = 'application/json'
             obj = {
    'status': 'True', 
    'content': the_page,
  }          
             print obj
 	     self.response.out.write(json.dumps(obj))


     def get(self):
	     headers = {'content-type': 'application/json'}
	     method = "GET"
	     url = "http://104.196.6.225:8080/"
	     req = urllib2.Request(url=url)
	     req.get_method = lambda: method
	     req.add_header('Content-Type', 'application/json')
	     f = urllib2.urlopen(req)
	     the_page_res = f.read()
             print 'length_of_json_string:', len(the_page_res), the_page_res[:50]
             self.response.headers['Content-Type'] = 'application/json'
             self.response.out.write(the_page_res)
             



app = webapp2.WSGIApplication([
    ('/submit_photo',HandlePhoto),('/', MainPageJquery),('/generate', HandlePhoto),], debug=True)
