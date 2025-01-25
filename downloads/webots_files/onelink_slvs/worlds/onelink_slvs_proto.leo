<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: https://leo-editor.github.io/leo-editor/leo_toc.html -->
<leo_file xmlns:leo="https://leo-editor.github.io/leo-editor/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20250125233710.2"><vh>original onlink_proto</vh></v>
<v t="leo.20250125233733.1"><vh>@clean onelink_leo.wbt</vh>
<v t="leo.20250126000845.1"><vh>VRML and PROTO</vh></v>
<v t="leo.20250126001100.1"><vh>WorldInfo Viewpoint and Texture</vh></v>
<v t="leo.20250126001114.1"><vh>Robot</vh>
<v t="leo.20250126001233.1"><vh>children</vh></v>
<v t="leo.20250126001238.1"><vh>controller</vh></v>
</v>
</v>
<v t="leo.20250125235802.1"><vh>@path ./../controllers/joint_controller</vh>
<v t="leo.20250125235721.1"><vh>@auto joint_controller.py</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20250125233710.2">#VRML_SIM R2023b utf8

EXTERNPROTO "../protos/TexturedBackground.proto"
EXTERNPROTO "../protos/TexturedBackgroundLight.proto"
EXTERNPROTO "../protos/RectangleArena.proto"
EXTERNPROTO "../protos/BaseSolid.proto"
EXTERNPROTO "../protos/JointSolid.proto"
EXTERNPROTO "../protos/LinkSolid.proto"

WorldInfo {}
Viewpoint {
  orientation -0.17911760145636924 0.20303955404969007 0.9626483388755317 1.7931226479511868
  position 0.7495096875887461 -3.1141998018989674 1.7796380905257032
}
TexturedBackground {}
TexturedBackgroundLight {}
RectangleArena {}

Robot {
  children [
    Solid {
      children [
        BaseSolid { }  # Instantiate the BaseSolid PROTO
        HingeJoint {
          jointParameters HingeJointParameters {
            axis 0 0 1
          }
          device [
            RotationalMotor {
              name "joint_motor"
            }
          ]
          endPoint Solid {
            children [
              JointSolid { }  # Instantiate the JointSolid PROTO
              Solid {
                children [
                  LinkSolid { }  # Instantiate the LinkSolid PROTO
                ]
              }
            ]
          }
        }
      ]
    }
  ]
  controller "joint_controller"
}</t>
<t tx="leo.20250125233733.1">@others
</t>
<t tx="leo.20250125235802.1"></t>
<t tx="leo.20250126000845.1">#VRML_SIM R2023b utf8

EXTERNPROTO "../protos/TexturedBackground.proto"
EXTERNPROTO "../protos/TexturedBackgroundLight.proto"
EXTERNPROTO "../protos/RectangleArena.proto"
EXTERNPROTO "../protos/BaseSolid.proto"
EXTERNPROTO "../protos/JointSolid.proto"
EXTERNPROTO "../protos/LinkSolid.proto"

</t>
<t tx="leo.20250126001100.1">WorldInfo {}
Viewpoint {
  orientation -0.17911760145636924 0.20303955404969007 0.9626483388755317 1.7931226479511868
  position 0.7495096875887461 -3.1141998018989674 1.7796380905257032
}
TexturedBackground {}
TexturedBackgroundLight {}
RectangleArena {}

</t>
<t tx="leo.20250126001114.1">Robot {
    @others
}
</t>
<t tx="leo.20250126001233.1">children [
    Solid {
        children [
            BaseSolid { }  # Instantiate the BaseSolid PROTO
            HingeJoint {
                jointParameters HingeJointParameters {
                    axis 0 0 1
                }

                device [
                    RotationalMotor {
                        name "joint_motor"
                    }
                ]
                endPoint Solid {
                    children [
                        JointSolid { }  # Instantiate the JointSolid PROTO
                        Solid {
                            children [
                                LinkSolid { }  # Instantiate the LinkSolid PROTO
                            ]
                        }
                    ]
                }
            }
        ]
    }
]
</t>
<t tx="leo.20250126001238.1">controller "joint_controller"</t>
</tnodes>
</leo_file>
