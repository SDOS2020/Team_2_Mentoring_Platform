const ChatWindow = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<div v-if="receiver === ''"class="card-header" style="border-radius: 10px 10px 0 0; background-color: lightgrey;">
			<center>
				<font size="4">
					Select a contact to start chatting
				</font>
			</center>
		</div>

		<div v-else class="card-header" style="border-radius: 10px 10px 0 0; background-color: lightgrey;">
			<center>
				<font size="4">
					Chat with <b>[[ receiver ]]</b>
				</font>
			</center>
		</div>

		<div class="msger-chat" style="height: 50vh; overflow-y: scroll; border: 2px solid #ddd;" id="chat-table">
			<table class="table table-borderless">
				<tbody>
					<tr v-for="message in messages">
						<div v-if="message.by_me" class="msg right-msg">
							<td>
								<div class="msg-bubble">
									<div class="msg-info">
										<div class="msg-info-name">You</div>
										<div class="msg-info-time">[[ message.date ]], [[ message.timestamp ]]</div>
									</div>

									<div class="msg-text">
										[[ message.content ]]
									</div>
								</div>
							</td>
						</div>
						<div v-else class="msg left-msg">
							<td>
								<div class="msg-bubble">
									<div class="msg-info">
										<div class="msg-info-name">[[ message.sender ]]</div>
										<div class="msg-info-time">[[ message.date ]], [[ message.timestamp ]]</div>
									</div>

									<div class="msg-text">
										[[ message.content ]]
									</div>
								</div>
							</td>
						</div>
					</tr>
				</tbody>
			</table>
		</div>
			
		<div v-if="receiver !== ''" class="input-group card-footer">
			<input @keyup.enter="send_message" type="text" class="form-control" v-model="message_to_send" placeholder="Type a message..." id="message-input-textbox">
			<div class="input-group-append">
				<button class="btn btn-outline-success" type="button" v-on:click="send_message">Send</button>
			</div>
		</div>
	</div>
	`,
	data() {
		return {
			messages: [],
			message_to_send: "",
		};
	},

	props: {
		receiver: {required: true},
		csrf: {required: true}
	},

	created() {
		this.get_messages();
		window.setInterval(this.get_messages, 1000);	
	},
	methods: {
		get_messages() {
			if (this.receiver.length === 0){
				return;
			}
			
			let request_url = "/api/get_messages/" + this.receiver;

			axios.get(request_url)
			.then(response => {
				this.messages = response.data.messages;
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
		},
		send_message() {
			if (this.message_to_send.length === 0) {
				return;
			}

			let msg = {
				'content': this.message_to_send,
				'receiver': this.receiver,
			}

			let request_url = "/api/send_message/";

			axios.post(request_url, {
				'message': msg
			},
			{
				headers: {
					'X-CSRFTOKEN': this.csrf
				}
			})
			.then(response => {})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});

			this.message_to_send = "";
			this.scroll_to_bottom();
			this.playAudio();
		},

		scroll_to_bottom() {
			let elem = document.getElementById("chat-table");
			elem.scrollTop = elem.scrollHeight;
		},

		playAudio() { 
			var x = document.getElementById("myAudio"); 
			x.play(); 
		} 
	},
};
