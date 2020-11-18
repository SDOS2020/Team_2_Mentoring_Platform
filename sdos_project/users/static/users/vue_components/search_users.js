const SearchUsers = {
	delimiters: ["[[", "]]"],
	components: {
		"tags-input": VoerroTagsInput,
	},
	template: `
	<div>
		<div class="input-group mb-3">
			<input type="text" class="form-control" maxlength="25" v-model="search_query" v-on:keyup="searchUsers">
			<div class="input-group-append">
				<button class="btn btn-outline-secondary" type="button" v-on:click="searchUsers">Search</button>
			</div>
		</div>

		<div>
			<input type="checkbox" v-model="mentors_allowed" value="Mentors" id="mentor-search" v-on:change="searchUsers">
			<label for="mentor-search">Mentors</label>
			<input type="checkbox" v-model="mentees_allowed" value="Mentees" id="mentee-search" v-on:change="searchUsers">
			<label for="mentee-search">Mentees</label>
		</div>


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
			search_query: "",
			search_results: [],
			mentors_allowed: true,
			mentees_allowed: false,

			// Role Tags
			existing_tags: [],
			selected_tags: [],
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_tags/";

		axios.get(request_url)
		.then(response => {
			this.existing_tags = response.data.tags;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});
	},
	methods: {
		tags_updated() {
			this.searchUsers();
		},
		searchUsers() {
			if (this.search_query.length === 0) {
				this.search_results = [];
				return;
			}

			let request_url = "http://127.0.0.1:8000/api/search_users";

			axios.get(request_url, {
				'params': {
					'pattern': this.search_query,
					'filters': JSON.stringify(this.selected_tags),
					'mentors_allowed': this.mentors_allowed,
					'mentees_allowed': this.mentees_allowed,
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
