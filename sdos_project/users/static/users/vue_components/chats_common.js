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
								<span class="d-none d-lg-block">
									<img class="img-fluid img-profile rounded-circle mx-auto mb-2" 
										src="https://cdn.business2community.com/wp-content/uploads/2017/08/blank-profile-picture-973460_640.png" 
										alt="Profile Picture"
										style="height: 2.5rem; width: 2.5rem; float: left" />
								</span>

								<div style="margin-top: 0.5rem;">
									&nbsp &nbsp[[ chatter.first_name ]] [[ chatter.last_name ]]
								</div>
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
