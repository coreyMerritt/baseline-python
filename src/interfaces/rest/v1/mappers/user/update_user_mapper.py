from interfaces.rest.v1.dto.req.user.update_user_req import UpdateUserReq
from interfaces.rest.v1.dto.res.user.update_user_res import UpdateUserRes
from services.models.inputs.user.update_user_sim import UpdateUserSIM
from services.models.outputs.user.update_user_som import UpdateUserSOM


class UpdateUserMapper:
  @staticmethod
  def req_to_sim(req: UpdateUserReq) -> UpdateUserSIM:
    return UpdateUserSIM(
      ulid=req.ulid,
      username=req.username,
      email_address=req.email_address,
      email_verified=req.email_verified,
      disabled=req.disabled
    )

  @staticmethod
  def som_to_res(som: UpdateUserSOM) -> UpdateUserRes:
    return UpdateUserRes(
      ulid=som.ulid,
      username=som.username,
      email_address=som.email_address
    )
