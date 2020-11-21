const ChatsCommon = {
	delimiters: ["[[", "]]"],
	components: {
		"chat-window": ChatWindow,
	},
	template: `
	<div>
		<table class="table table-borderless">
			<tbody>	
				<tr>
					<td>
						<ul class="list-group">
							<li 
							class="list-group-item"
							style="border-radius: 10px 10px 0 0; background-color: lightgrey; border: none;"
							>
							<center>Contacts</center>
							</li>
							
							<li v-on:click="active_chatter=chatter.username" 
								v-for="chatter in chatters" 
								v-bind:class="[ active_chatter === chatter.username ? 'active' : '' ]"
								class="list-group-item" 
								style="cursor: pointer;"
							>
								[[ chatter.username ]]
							</li>
						</ul>
					</td>
					<td style="width: 80%;">
						<chat-window v-bind:receiver="active_chatter" sender="{{ user.username }}" v-bind:csrf="csrf">
						</chat-window>
					</td>
				</tr>
			</tbody>
		</table>

	</div>
	`,
	props: {
		csrf: {required: true}
	},
	data() {
		return {
			chatters: [],
			active_chatter: "",
		};

	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_chatters/";

		axios.get(request_url)
		.then(response => {
			this.chatters = response.data.chatters;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});
	},


};
