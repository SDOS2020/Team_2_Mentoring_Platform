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
							<option value="1">One Meeting</option>
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

				<tr>
					<td>
						<p class="lead">
							Mentees you wish to mentor
						</p>
					</td>
					<td>
						<ul style="list-style: none; padding: 0px">
							<li>
								<input v-model="will_mentor_faculty" type="checkbox">
								Faculty
							</li>

							<li>
								<input v-model="will_mentor_phd" type="checkbox">
								PhD
							</li>

							<li>
								<input v-model="will_mentor_mtech" type="checkbox">
								MTech
							</li>

							<li>
								<input v-model="will_mentor_btech" type="checkbox">
								BTech
							</li>
						</ul>
					</td>
				</tr>

				<tr>
					<td colspan=2>
						<p class="lead">
							You are willing to
						</p>
						<ul style="list-style: none; padding: 0px">
							<li v-for="(reponsibility, i) in responsibilities">
								<input v-model="willing_to[i]" type="checkbox">
								[[ reponsibility[1] ]]
							</li>
						</ul>
					</td>
				</tr>

				<tr>
					<td colspan=2>
						<p class="lead">
							Anything else you can help the mentees with
						</p>
						<textarea style="width: 100%" v-model="other_responsibility" />
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
			will_mentor_faculty: false,
			will_mentor_phd: false,
			will_mentor_mtech: false,
			will_mentor_btech: false,
			willing_to: [false, false, false, false, false, false, false, false],
			responsibilities: [],
			other_responsibility: '',
		};
	},
	props: {
		csrf: { 'required': true }
	},
	created() {
		request_url = "/api/get_settings/";

		axios.get(request_url)
		.then(response => {
			this.mentorship_duration = response.data.mentorship_duration;
			this.is_open_to_mentorship = response.data.is_open_to_mentorship;
			this.will_mentor_faculty = response.data.will_mentor_faculty;
			this.will_mentor_phd = response.data.will_mentor_phd;
			this.will_mentor_mtech = response.data.will_mentor_mtech;
			this.will_mentor_btech = response.data.will_mentor_btech;
			this.responsibilities = response.data.responsibilities;
			for (let i = 0; i < 8; ++i) {
				this.willing_to[i] = this.responsibilities[i][0];
			}
			this.other_responsibility = response.data.other_responsibility;
			console.log(this.willing_to);
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
			let request_url = "/api/update_settings/";

			axios.post(request_url, {
				'mentorship_duration': this.mentorship_duration,
				'is_open_to_mentorship': this.is_open_to_mentorship,
				'will_mentor_faculty' : this.will_mentor_faculty,
				'will_mentor_phd' : this.will_mentor_phd,
				'will_mentor_mtech' : this.will_mentor_mtech,
				'will_mentor_btech' : this.will_mentor_btech,
				'willing_to': this.willing_to,
				'other_responsibility': this.other_responsibility,
			}, {
				headers: {'X-CSRFTOKEN': this.csrf}
			})
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
