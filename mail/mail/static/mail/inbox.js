document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  // document.querySelector('form').onsubmit=fetch('/emails', {
  //   method: 'POST',
  //   body: JSON.stringify({
  //       recipients: document.querySelector('#compose-recipients').value,
  //       subject:document.querySelector('#compose-subject').value,
  //       body: document.querySelector('#compose-body').value
  //   })
  // })
  // .then(response => response.json())
  // .then(result => {
  //     //document.querySelector('#compose-view').innerHTML=``
  //     console.log(result);
  // });
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose-form').addEventListener('submit', submit_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}


function submit_email(event){
  event.preventDefault()
  //post email to api route...
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject:document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
   .then(response => response.json())
   .then(result=> {
     if(result.error){
         alert(result.error),
         compose_email();
     }
     else{
     alert(result.message),
    load_mailbox('sent')
    }
  })
   
  // .then(result => {
  //     //document.querySelector('#compose-view').innerHTML=``
  //     console.log(result);
  // });
}
function load_email(id,mailbox)
{
fetch('/emails/'+id)
.then(response => response.json())
.then(email => {
        //show email and hide compose-view and email-view
        document.querySelector('#emails-view').style.display = 'none';
        document.querySelector('#compose-view').style.display = 'none';
        document.querySelector('#email-view').style.display = 'block';

        //display email
        const view=document.querySelector('#email-view');
        view.className="card";
        view.innerHTML=`
        <ul class="list-group">
          <li class="list-group-item"><b>From:</b><span>${email['sender']}</span>
          <li class="list-group-item"><b>To:</b><span>${email['recipients']}</span>
          <li class="list-group-item"><b>Subject:</b><span>${email['subject']}</span>
          <li class="list-group-item"><b>Time:</b><span>${email['timestamp']}</span>
        </ul>

        <p class="m-2">${email['body']}</p>
        <hr>

        `;
        
        const reply=document.createElement('button');
        reply.className="btn btn-success m-1";
        reply.innerHTML='reply'
        reply.addEventListener('click',function(){
          compose_email();
          // populate feilds
          let subject=email['subject'];
          document.querySelector('#compose-recipients').value =`${email['sender']}`;
          if(!subject.includes("Re: "))
            document.querySelector('#compose-subject').value = `Re: ${subject}`;
          else
          document.querySelector('#compose-subject').value = subject;
          document.querySelector('#compose-body').value = '';
          
        })
        view.appendChild(reply);
        if(mailbox!='sent'){
          const archiveb=document.createElement('button');
          archiveb.className="btn btn-primary m-1";
          archiveb.innerHTML=!email['archived']?'Archive':'unarchive';
          archiveb.addEventListener('click',function() {
            fetch('/emails/'+email['id'], {
              method: 'PUT',
              body: JSON.stringify({
                  archived: !email['archived']
              })
            }).then(response => load_mailbox('inbox'))
          })
          view.appendChild(archiveb)
        }
        
        //creating unread button
        const readb=document.createElement('button');
        readb.className="btn btn-primary m-1";
        readb.innerHTML=!email['read']?'mark read':'mark as unread';
        readb.addEventListener('click',function() {
          fetch('/emails/' + email['id'], {
            method: 'PUT',
            body: JSON.stringify({
                read: false
            })
          }).then(response => load_mailbox('inbox'))
        })
        view.appendChild(readb)
      });
        
     
}
function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  const view=document.querySelector('#emails-view');
  view.innerHTML=`<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  fetch('/emails/'+ mailbox)
  .then(response => response.json())
  .then(emails => {
      // genrate div for each emails
      emails.forEach(email => {
        let div=document.createElement('div');
        div.className="card";
        //div.style.border-radius='25px';
       // div.className=email['read']? "element-list-item-read":"element-list-item-unread";
        if(!email['read'])
        {
         div.style.backgroundColor='white';
        }
        if(email['read'])
        {
         div.style.backgroundColor='grey';
        }
        
        div.innerHTML=`
        <span class="sender  col-6"><b>${email['sender']}</b></span>
        <span class="subject col-6"><b>${email['subject']}</b></span>
        <span class="timestamp col-6"><small>${email['timestamp']}</small></span>`;
        //add eventlistner and append to dom
        // var flag=0;
        // if(mailbox=='sent')
        // {
        //   flag=1;
        // }
        const id=email['id'];
        div.addEventListener('click',()=>load_email(email['id'],mailbox));
        
        
        view.appendChild(div);
        //creating unread button
        const readb=document.createElement('button');
        readb.className="btn btn-primary m-1";
        readb.innerHTML=!email['read']?'mark read':'mark as unread';
        readb.addEventListener('click',function() {
          fetch('/emails/' + email['id'], {
            method: 'PUT',
            body: JSON.stringify({
                read: !email['read']
            })
          }).then(response => load_mailbox('inbox'))
        })
        view.appendChild(readb)
       
        
      

        
        
      });
      
  });
}