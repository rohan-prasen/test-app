async function getConversationTips() {
 const meetingWith = document.getElementById('meetingWith').value;
 const agenda = document.getElementById('agenda').value;
 const tipsOutput = document.getElementById('tipsOutput');

 if (!meetingWith || !agenda) {
 tipsOutput.textContent = 'Please enter both meeting person and agenda.';
 return;
 }

 const prompt = `Meeting with ${meetingWith}, Agenda of the meeting... ${agenda}`;

 tipsOutput.textContent = 'Generating tips...';

 try {
 const response = await fetch('/generate', {
 method: 'POST',
 headers: {
 'Content-Type': 'application/json',
 },
 body: JSON.stringify({ prompt: prompt }),
 });

 const data = await response.json();

 if (response.ok) {
 tipsOutput.textContent = data.response;
 } else {
 tipsOutput.textContent = `Error: ${data.error}`;
 }
 } catch (error) {
 tipsOutput.textContent = `Error: ${error}`;
 }
}

