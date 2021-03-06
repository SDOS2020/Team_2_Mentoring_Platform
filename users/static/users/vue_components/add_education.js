const AddEducation = {
	delimiters: ["[[", "]]"],
	template: `
		<div>
			<font size="5">Education</font>
			<a
				class="btn btn-sm btn-primary"
				data-toggle="modal"
				data-target="#addEduModalLong"
				style="float: right;"
			>
				Add More
			</a>
			<hr>

			<!-- START MODAL - addEduModal -->
			<div class="modal fade" id="addEduModalLong" tabindex="-1" role="dialog" aria-labelledby="addEduModalLongTitle" aria-hidden="true">
				<div class="modal-dialog" role="document">
					<div class="modal-content">
						<div class="modal-header">
							<h5 class="modal-title" id="addEduModalLongTitle">Add Education</h5>
							<button type="button" class="close" data-dismiss="modal" aria-label="Close">
								<span aria-hidden="true">&times;</span>
							</button>
						</div>

						<div class="modal-body">
							<h5>Qualification</h5>
							<input v-model="qualification" class="form-control" style="width: 100%;">
						</div>
							
						<div class="modal-body">
							<h5>Start Date</h5>
							<input v-model="start_date" type="date" class="form-control" required>
						</div>
							
						<div class="modal-body">
							<h5>End Date</h5>
							<input v-model="end_date" type="date" class="form-control" required>
						</div>
						
						<div class="modal-body">
							<h5>Organization</h5>
							<input v-model="organization" class="form-control" style="width: 100%;">
						</div>

						<div class="modal-body">
							<h5>A brief description</h5>
							<textarea v-model="detail" class="form-control" style="width: 100%;"></textarea>
						</div>

						<div class="modal-footer">
							<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
							<button
								v-on:click="add_education()"
								type="button"
								class="btn btn-success"
								data-dismiss="modal"
							>
								Add
							</button>
						</div>
					</div>
				</div>
			</div>
			<!-- END MODAL -->

			<table class="table table-hover table-light table-sm">
				<tr v-for="(_, i) in qualifications.length" :key="i">
					<td>
						<div style="float: right;">
							<i>
								[[ start_dates[i] ]] <b>to</b>
								<br>
								[[ end_dates[i] ]]
							</i>
						</div>
						
						<div style="width: 70%">
							<b> [[ qualifications[i] ]] </b>
						</div>

						<br/>
						<b> [[ organizations[i] ]] </b>
						<br/>
						[[ details[i] ]]
						<hr>
					</td>
				</tr>
			</table>
		</div>
	`,

	data () {
		return {
			qualification: '',
			start_date: '',
			end_date: '',
			organization: '',
			detail: '',
		}
	},
	
	props: {
		qualifications: {required: true},
		start_dates: {required: true},
		end_dates: {required: true},
		organizations: {required: true},
		details: {required: true},
	},

	methods: {
		limit_content_size(content, lower, upper, type) {
			if (content.length < lower) {
				alert('[ERROR] Please elaborate on ' + type);
				return false;
			}

			if (content.length > upper) {
				alert('[ERROR] Please shorten the content of ' + type);
				return false;
			}

			return true;
		},

		add_education() {
			if (!this.limit_content_size(this.qualification, 2, 128, 'Qualification')) { return ; }
			if (!this.limit_content_size(this.start_date, 4, 128, 'Start Date')) { return ; }
			if (!this.limit_content_size(this.end_date, 4, 128, 'End Date')) { return ; }
			if (!this.limit_content_size(this.organization, 4, 128, 'Organization')) { return ; }
			if (!this.limit_content_size(this.detail, 0, 512, 'Detail')) { return ; }

			let sd = new Date(this.start_date);
			let ed = new Date(this.end_date);

			if (sd > ed) {
				alert('[ERROR] Start date must be less than End date');
				return ;
			}

			this.$emit('update_education',
				this.qualification,
				this.start_date,
				this.end_date,
				this.organization,
				this.detail
			);

			this.qualification = "";
			this.start_date = "";
			this.end_date = "";
			this.organization = "";
			this.detail = "";
		}
	}
}