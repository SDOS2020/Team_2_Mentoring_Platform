const ChatWindow = {
	delimiters: ["[[", "]]"],
	template: `
	<div class="col-md-6">
		<div class="card-header">
			<font size="5">Chat with <b>[[ receiver ]]</b></font>
		</div>
		<div class="msger-chat" style="height: 65vh; overflow-y: scroll; border: 2px solid #ddd;" id="chat-table">
			<table class="table table-borderless">
				<tbody>
					<tr v-for="message in messages">
						<div v-if="message.by_me" class="msg right-msg">
							<td>
								<div class="msg-bubble">
									<div class="msg-info">
										<div class="msg-info-name">You</div>
										<div class="msg-info-time">[[ message.timestamp ]]</div>
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
										<div class="msg-info-time">[[ message.timestamp ]]</div>
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
			
		<div class="input-group mb-3 card-footer">
			<input type="text" class="form-control" v-model="message_to_send" placeholder="Type a message...">
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
		sender: {required: true},
		csrf: {required: true}
	},

	created() {
		this.get_messages();
		window.setInterval(this.get_messages, 1000);	
	},
	methods: {
		get_messages() {
			let request_url = "http://127.0.0.1:8000/api/get_messages/" + this.receiver;

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

			let request_url = "http://127.0.0.1:8000/api/send_message/";

			axios.post(request_url, 
				{'message': msg}, 
				{headers: {'X-CSRFTOKEN': this.csrf}})
			.then(response => {
				console.log('Success!!!!');
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});

			this.message_to_send = "";
			this.scroll_to_bottom();

		},

		scroll_to_bottom() {
			let elem = document.getElementById("chat-table");
			elem.scrollTop = elem.scrollHeight;
		}
		
	},

	updated() {
		
	}
};
