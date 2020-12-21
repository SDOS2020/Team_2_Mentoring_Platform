const MentorSettings = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<table class="table">
			<tbody>
				<tr>
					<td>
						<p class="lead">
							What is your tentative mentorship duration?
						</p>
					</td>
					<td>
						<select v-model="mentorship_duration" name="mentorship_duration" id="mentorship_duration">
							<option value="3">3 Months</option>
							<option value="6">6 Months</option>
							<option value="9">9 Months</option>
							<option value="12">12 Months</option>
							<option value="15">15 Months</option>
						</select>
					</td>
				</tr>

				<tr>
					<td>
						<p class="lead">
							Are you open to taking up new mentees?
						</p>
					</td>
					<td>
						<input v-model="is_open_to_mentorship" type="checkbox" id="is_open_for_mentoring" name="is_open_for_mentoring">
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
			is_open_to_mentorship: true,
			mentorship_duration: 2,
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
			this.mentorship_duration = response.data.mentorship_duration;
			this.is_open_to_mentorship = response.data.is_open_to_mentorship;
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

			axios.post(request_url, 
				{'mentorship_duration': this.mentorship_duration,
				'is_open_to_mentorship': this.is_open_to_mentorship}, 
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
