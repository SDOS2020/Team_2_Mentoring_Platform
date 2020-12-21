const SearchUsers = {
	delimiters: ["[[", "]]"],
	components: {
		"tags-input": VoerroTagsInput,
	},
	template: `
	<div>
		<!-- Tags -->
		<tags-input element-id="search-tags"
			v-model="selected_tags"
			v-bind:existing-tags="existing_tags"
			v-bind:typeahead="true"
			v-on:tags-updated="tags_updated"
		>
		</tags-input>

		<br />
		<div style="height: 100%; overflow-y: scroll;">
			<table class="table table-hover">
				<thead style="background-color: white;">
					<tr>
						<th scope="col">#</th>
						<th scope="col">Username</th>
						<th scope="col">Role</th>
						<th scope="col">Actions</th>
					</tr>
				</thead>
				<tbody>
					<tr v-for="(result, index) in search_results" v-bind:key="result.id">
						<td>
							[[ index + 1 ]]
						</td>

						<td>
							<a :href="'//127.0.0.1:8000/users/profile/' + result.username">
								[[ result.username ]]
							</a>
						</td>

						<td>
							<button v-if="result.is_mentor" class="btn btn-sm btn-secondary" disabled>
								Mentor
							</button>
							<button v-else class="btn btn-sm btn-secondary" disabled>
								Mentee
							</button>
						</td>

						<td>
							<div v-if="result.status === 0">
							</div>
							<div v-if="result.status === 1">
								<button class="btn btn-sm btn-primary" v-on:click="sendRequest(result.username)"> Request Mentorship </button>
							</div>
							<div v-if="result.status === 2">
								<button class="btn btn-sm btn-primary" v-on:click="sendRequest(result.username)"> Request Menteeship </button>
							</div>
							<div v-if="result.status === 3">
								<button class="btn btn-sm btn-warning" disabled> Pending Request </button>
							</div>
							<div v-if="result.status === 4">
								<button class="btn btn-sm btn-secondary" disabled> Request Received </button>
							</div>
							<div v-if="result.status === 5">
								<button class="btn btn-sm btn-info" disabled> Mentee </button>
							</div>
							<div v-if="result.status === 6">
								<button class="btn btn-sm btn-info" disabled> Mentor </button>
							</div>
						</td>

					</tr>
				</tbody>
			</table>
		</div>
	</div>
	`,
	data() {
		return {
			search_results: [],
			existing_tags: [],
			selected_tags: [],
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_mentor_tags/";

		axios.get(request_url)
		.then(response => {
			this.existing_tags = response.data.tags;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});
		this.searchUsers();

	},
	methods: {
		tags_updated() {
			this.searchUsers();
		},
		searchUsers() {
			let request_url = "http://127.0.0.1:8000/api/search_users";

			axios.get(request_url, {
				'params': {
					'filters': JSON.stringify(this.selected_tags),
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				if (response.data.length > 30) {
					console.log("Too many results: " + response.data.length);
					console.log("Showing only top 30");
					this.search_results = response.data.slice(0, 30);
				}
				else {
					this.search_results = response.data;
				}
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
				this.search_results = [];
			});
		},
		sendRequest(username) {
			let request_url = "http://127.0.0.1:8000/api/send_request";

			axios.get(request_url, {
				'params': {
					'requestee': username
				}
			})
			.then(response => {
				console.log("[SUCCESS]");
				for (result of this.search_results) {
					if (result.username === username) {
						result.status = 3;
						break;
					}
				}
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
		}
	}
};
