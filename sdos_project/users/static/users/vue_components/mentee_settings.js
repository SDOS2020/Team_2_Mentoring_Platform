const MenteeSettings = {
	delimiters: ["[[", "]]"],
	components: {
		"tags-input": VoerroTagsInput,
	},
	template: `
	<div>
		<table class="table">
			<tbody>
				<tr>
					<td>
						<p class="lead">
							What kind of mentors are you looking for?
						</p>
					</td>
					<td style="width: 30vw;">
						<tags-input element-id="settings-tags"
							v-model="selected_tags"
							v-bind:existing-tags="existing_tags"
							v-bind:typeahead="true"
						>
						</tags-input>
					</td>
				</tr>

				<tr>
					<td>
						<p class="lead">
							Are you ready to be a mentee?
						</p>
					</td>
					<td>
						<input v-model="needs_mentoring" type="checkbox" id="needs_mentoring" name="needs_mentoring">
					</td>
				</tr>

				<tr>
					<td>
						<p class="lead">
							Do you need urgent mentorship?
						</p>
					</td>
					<td>
						<input v-model="needs_urgent_mentoring" type="checkbox" id="needs_urgent_mentoring" name="needs_urgent_mentoring">
					</td>
				</tr>

			</tbody>
		</table>

		<table>
			<tr>
				<td> <button class="btn btn-success" v-on:click="update_settings">Save Changes</button> </td>
				<td>
					<div v-if="update_success">
						<i style="color: green; font-size: 2rem; margin-left: 1rem" class="fas fa-check-circle"></i>
					</div>
				</td>
			</tr>
		</table>

	</div>
	`,
	data() {
		return {
			selected_tags: [],
			existing_tags: [],
			needs_urgent_mentoring: true,
			needs_mentoring: true,
			update_success: false,
		};
	},
	created() {
		let request_url = "http://127.0.0.1:8000/api/get_my_tags/";

		axios.get(request_url)
		.then(response => {
			this.selected_tags = response.data['my_tags'];
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});

		request_url = "http://127.0.0.1:8000/api/get_mentee_tags/";

		axios.get(request_url)
		.then(response => {
			this.existing_tags = response.data.tags;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});

		request_url = "http://127.0.0.1:8000/api/get_settings/";

		axios.get(request_url)
		.then(response => {
			this.needs_mentoring = response.data.needs_mentoring;
			this.needs_urgent_mentoring = response.data.needs_urgent_mentoring;
		})
		.catch(error => {
			console.log("[ERROR]");
			console.log(error);
		});
	},
	props: {
		csrf: {'required': true}
	},
	methods: {
		update_settings() {
			this.update_my_tags();
			this.update_other_settings();

			this.update_success = true;
			window.setTimeout(this.hide_button, 1000);
		},

		hide_button() {
			this.update_success = false;
		},

		update_my_tags() {
			let request_url = "http://127.0.0.1:8000/api/update_my_tags/";

			axios.post(request_url, 
				{'updated_tags': this.selected_tags}, 
				{headers: {'X-CSRFTOKEN': this.csrf}})
			.then(response => {
				// this.existing_tags = response.data.tags;
				console.log('Success!!!!');
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});
		},

		update_other_settings() {
			let request_url = "http://127.0.0.1:8000/api/update_settings/";

			axios.post(request_url, 
				{'needs_mentoring': this.needs_mentoring,
				'needs_urgent_mentoring': this.needs_urgent_mentoring}, 
				{headers: {'X-CSRFTOKEN': this.csrf}})
			.then(response => {
				// this.existing_tags = response.data.tags;
				console.log('Success!!!!');
			})
			.catch(error => {
				console.log("[ERROR]");
				console.log(error);
			});

		}
	}
};
