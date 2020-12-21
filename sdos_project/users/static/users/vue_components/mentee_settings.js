const MenteeSettings = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<table class="table">
			<tbody>
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
			needs_urgent_mentoring: true,
			needs_mentoring: true,
			update_success: false,
		};
	},
	props: {
		csrf: { 'required': true }
	},
	created() {
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
	methods: {
		update_settings() {
			this.update_other_settings();
			this.update_success = true;
			window.setTimeout(this.hide_button, 1000);
		},

		hide_button() {
			this.update_success = false;
		},

		update_other_settings() {
			let request_url = "http://127.0.0.1:8000/api/update_settings/";

			axios.post(request_url, {
				'needs_mentoring': this.needs_mentoring,
				'needs_urgent_mentoring': this.needs_urgent_mentoring}, 
				{
					headers: {
						'X-CSRFTOKEN': this.csrf
					}
				}
			)
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
